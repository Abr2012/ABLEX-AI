
const chatForm = document.getElementById("chat-form");
const userInput = document.getElementById("user-input");
const chatMessages = document.getElementById("chat-messages");

chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const message = userInput.value.trim();

    if (!message) return;

    // Display the user's message
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = message;
    chatMessages.appendChild(userMessage);

    userInput.value = "";

    // Show loading message
    const loading = document.createElement("div");
    loading.className = "bot-message";
    loading.textContent = "ABLEX is thinking...";
    chatMessages.appendChild(loading);

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        loading.textContent = data.reply || data.error || "Sorry, something went wrong.";

    } catch (error) {
        loading.textContent = "Unable to connect. Please try again.";
    }

    chatMessages.scrollTop = chatMessages.scrollHeight;
});
