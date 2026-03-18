const API_URL = "http://localhost:8000/api/chat";

async function sendMessage() {
    const input = document.getElementById("input");
    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();
    if (!message) return;

    appendMessage("You", message);
    input.value = "";

    const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await res.json();

    appendMessage("Bot", data.answer);
}

function appendMessage(sender, text) {
    const chatBox = document.getElementById("chat-box");
    const div = document.createElement("div");
    div.className = "message";
    div.innerText = `${sender}: ${text}`;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}