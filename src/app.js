import { LocalVoiceAgent, SUPPORT_MESSAGE } from "./agent-core.js";

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition || null;

const statusCard = document.querySelector("[data-status-card]");
const statusLabel = document.querySelector("[data-status]");
const transcriptLog = document.querySelector("[data-transcript]");
const remindersList = document.querySelector("[data-reminders]");
const startButton = document.querySelector("[data-start]");
const stopButton = document.querySelector("[data-stop]");
const textForm = document.querySelector("[data-text-form]");
const textInput = document.querySelector("[data-text-input]");
const muteToggle = document.querySelector("[data-mute]");
const supportNotice = document.querySelector("[data-support-notice]");

const agent = new LocalVoiceAgent();
let recognition = null;
let isListening = false;
let isMuted = false;

function setStatus(message, tone = "idle") {
  statusLabel.textContent = message;
  statusCard.dataset.tone = tone;
  statusLabel.dataset.tone = tone;
}

function addTranscript(role, text) {
  const item = document.createElement("li");
  item.className = `transcript-item transcript-item--${role}`;

  const speaker = document.createElement("span");
  speaker.className = "transcript-speaker";
  speaker.textContent = role === "agent" ? agent.name : "You";

  const message = document.createElement("p");
  message.textContent = text;

  item.append(speaker, message);
  transcriptLog.append(item);
  transcriptLog.scrollTop = transcriptLog.scrollHeight;
}

function renderReminders(reminders) {
  remindersList.replaceChildren();

  if (!reminders.length) {
    const empty = document.createElement("li");
    empty.className = "empty-state";
    empty.textContent = "No reminders yet.";
    remindersList.append(empty);
    return;
  }

  for (const reminder of reminders) {
    const item = document.createElement("li");
    item.textContent = reminder;
    remindersList.append(item);
  }
}

function speak(text) {
  if (isMuted || !("speechSynthesis" in window)) {
    return;
  }

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);
  utterance.rate = 0.95;
  utterance.pitch = 1;
  window.speechSynthesis.speak(utterance);
}

function handleUserInput(text) {
  const cleaned = text.trim();

  if (!cleaned) {
    return;
  }

  addTranscript("user", cleaned);

  if (/^(stop speaking|be quiet|mute)$/i.test(cleaned)) {
    window.speechSynthesis?.cancel();
    isMuted = true;
    muteToggle.checked = true;
    setStatus("Muted", "idle");
    addTranscript("agent", "Muted. Turn speech back on when you are ready.");
    return;
  }

  const result = agent.respond(cleaned);
  addTranscript("agent", result.response);
  renderReminders(result.reminders);
  speak(result.response);
}

function createRecognition() {
  if (!SpeechRecognition) {
    startButton.disabled = true;
    stopButton.disabled = true;
    supportNotice.hidden = false;
    supportNotice.textContent = SUPPORT_MESSAGE;
    setStatus("Speech recognition unavailable", "warning");
    return null;
  }

  const instance = new SpeechRecognition();
  instance.continuous = true;
  instance.interimResults = true;
  instance.lang = navigator.language || "en-US";

  instance.addEventListener("start", () => {
    isListening = true;
    startButton.disabled = true;
    stopButton.disabled = false;
    setStatus("Listening...", "active");
  });

  instance.addEventListener("end", () => {
    isListening = false;
    startButton.disabled = false;
    stopButton.disabled = true;
    setStatus("Ready", "idle");
  });

  instance.addEventListener("error", (event) => {
    setStatus(`Microphone error: ${event.error}`, "warning");
  });

  instance.addEventListener("result", (event) => {
    let finalTranscript = "";

    for (let index = event.resultIndex; index < event.results.length; index += 1) {
      const result = event.results[index];
      if (result.isFinal) {
        finalTranscript += result[0].transcript;
      }
    }

    if (finalTranscript) {
      handleUserInput(finalTranscript);
    }
  });

  return instance;
}

startButton.addEventListener("click", () => {
  if (!recognition || isListening) {
    return;
  }

  recognition.start();
});

stopButton.addEventListener("click", () => {
  recognition?.stop();
  window.speechSynthesis?.cancel();
});

muteToggle.addEventListener("change", (event) => {
  isMuted = event.target.checked;
  if (isMuted) {
    window.speechSynthesis?.cancel();
  }
});

textForm.addEventListener("submit", (event) => {
  event.preventDefault();
  handleUserInput(textInput.value);
  textInput.value = "";
  textInput.focus();
});

recognition = createRecognition();
renderReminders(agent.getSnapshot().reminders);
addTranscript("agent", `Hi, I am ${agent.name}. Press Start listening or type a command below.`);
