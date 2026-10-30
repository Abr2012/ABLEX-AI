const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const statusText = document.getElementById("status");
const transcriptText = document.getElementById("transcript");
const replyText = document.getElementById("reply");

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

let recognition = null;
let active = false;
let speaking = false;

if (!SpeechRecognition) {
  statusText.textContent =
    "Speech recognition is not supported in this browser. Try Chrome.";
  startButton.disabled = true;
} else {
  recognition = new SpeechRecognition();
  recognition.lang = "en-IN";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => {
    statusText.textContent = "🎙️ Listening...";
  };

  recognition.onresult = (event) => {
    const text = event.results[event.results.length - 1][0].transcript;
    transcriptText.textContent = "You: " + text;

    // Temporary test: show recognized speech.
    statusText.textContent = "Speech recognized!";
  };

  recognition.onerror = (event) => {
    statusText.textContent = "Microphone error: " + event.error;
  };

  recognition.onend = () => {
    if (active && !speaking) {
      statusText.textContent = "Ready for your next question.";
    }
  };
}

startButton.addEventListener("click", () => {
  if (!recognition) return;

  active = true;
  startButton.disabled = true;
  stopButton.disabled = false;

  recognition.start();
});

stopButton.addEventListener("click", () => {
  active = false;

  if (recognition) {
    recognition.stop();
  }

  window.speechSynthesis.cancel();

  startButton.disabled = false;
  stopButton.disabled = true;
  statusText.textContent = "Conversation stopped.";
});
