const sendButton = document.querySelector("#submit");
const container = document.querySelector(".chat-body");
const inputField = document.querySelector("#input");

function appendMessage(text, className) {
    const bubble = document.createElement("div");
    bubble.className = className;
    bubble.innerText = text;
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
}

async function sendMessage() {
    const input = inputField.value.trim();
    if (!input) {
        return;
    }

    appendMessage(input, "user_input");
    inputField.value = "";
    sendButton.disabled = true;

    try {
        const response = await fetch("/BuddyBot", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ Input: input })
        });

        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || "Unable to get a response right now.");
        }

        appendMessage(data.message, "message-bubble");
    } catch (error) {
        appendMessage(error.message, "message-bubble");
    } finally {
        sendButton.disabled = false;
        inputField.focus();
    }
}

sendButton.addEventListener("click", (event) => {
    event.preventDefault();
    sendMessage();
});

inputField.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
