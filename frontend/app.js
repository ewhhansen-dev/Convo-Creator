// The Dictator - Frontend Logic

const STATUS = document.getElementById('status');
const TXT_OUTPUT = document.getElementById('transcript');
const BTN_RECORD = document.getElementById('btnRecord');
const BTN_COPY = document.getElementById('btnCopy');

let mediaRecorder;
let audioChunks = [];
let isRecording = false;

// --- Audio Recording ---

async function setupAudio() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];
            await sendAudio(audioBlob);
        };

        console.log("Audio initialized.");
    } catch (err) {
        console.error("Error accessing microphone:", err);
        STATUS.innerText = "Error: Mic access denied.";
    }
}

function toggleRecording() {
    if (!mediaRecorder) return;

    if (isRecording) {
        // Stop
        mediaRecorder.stop();
        isRecording = false;
        BTN_RECORD.innerText = "Record";
        BTN_RECORD.classList.remove("recording");
        STATUS.innerText = "Processing...";
    } else {
        // Start
        mediaRecorder.start();
        isRecording = true;
        BTN_RECORD.innerText = "Stop";
        BTN_RECORD.classList.add("recording");
        STATUS.innerText = "Recording...";
    }
}

// --- Backend API ---

async function sendAudio(blob) {
    const formData = new FormData();
    formData.append("file", blob, "recording.wav");

    try {
        const response = await fetch("http://localhost:8000/transcribe", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Backend error");

        const data = await response.json();
        const text = data.text;

        if (text) {
            TXT_OUTPUT.value += (TXT_OUTPUT.value ? "\n" : "") + text;
            STATUS.innerText = "Ready";
            copyToClipboard(text); // Auto-copy latest? Maybe just manual.
        } else {
            STATUS.innerText = "Ready (No speech detected)";
        }
    } catch (err) {
        console.error(err);
        STATUS.innerText = "Error: Backend unreachable";
    }
}

function copyToClipboard(text = null) {
    const content = text || TXT_OUTPUT.value;
    navigator.clipboard.writeText(content).then(() => {
        STATUS.innerText = "Copied to clipboard!";
        setTimeout(() => STATUS.innerText = "Ready", 2000);
    });
}

// --- MIDI Integration (Web MIDI API) ---

function setupMidi() {
    if (!navigator.requestMIDIAccess) {
        STATUS.innerText += " (Web MIDI not supported)";
        return;
    }

    navigator.requestMIDIAccess().then(onMidiSuccess, onMidiFailure);
}

function onMidiSuccess(midiAccess) {
    STATUS.innerText = "Ready (MIDI Connected)";
    for (var input of midiAccess.inputs.values()) {
        input.onmidimessage = getMidiMessage;
    }
}

function onMidiFailure() {
    STATUS.innerText += " (MIDI Access Failed)";
}

function getMidiMessage(message) {
    var command = message.data[0];
    var note = message.data[1];
    var velocity = (message.data.length > 2) ? message.data[2] : 0;

    // Note On (usually 144-159) with Velocity > 0
    if (command >= 144 && command <= 159 && velocity > 0) {
        handleMidiNote(note);
    }
}

function handleMidiNote(note) {
    console.log("MIDI Note:", note);
    // Default Map (matches README)
    // Pad 1 (36): Toggle Recording
    if (note === 36) {
        toggleRecording();
    }
    // Pad 2 (37): Copy
    else if (note === 37) {
        copyToClipboard();
    }
}

// --- Init ---

window.addEventListener('DOMContentLoaded', () => {
    setupAudio();
    setupMidi();

    BTN_RECORD.addEventListener('click', toggleRecording);
    BTN_COPY.addEventListener('click', () => copyToClipboard());
});
