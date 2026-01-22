// --------------------
// DOM Elements
// --------------------
const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

// --------------------
// Helper: add message
// --------------------
function addMessage(text, sender) {
    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender);
    msgDiv.innerHTML = text;
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return msgDiv;
}

// --------------------
// Send Question
// --------------------
function sendQuestion() {
    const question = userInput.value.trim();
    if (!question) return;

    // Show user message
    addMessage(question, "user");
    userInput.value = "";

    // Bot placeholder
    const botDiv = addMessage("<em>Thinking...</em>", "bot");

    // Open SSE connection
    const eventSource = new EventSource(
        `/stream?question=${encodeURIComponent(question)}`
    );

    let fullAnswer = "";

    eventSource.onmessage = function (event) {

        // --------------------
        // STATUS messages
        // --------------------
        if (event.data.startsWith("__STATUS__::")) {
            const statusText = event.data.replace("__STATUS__::", "");
            botDiv.innerHTML = `<em>${statusText}</em>`;
            chatWindow.scrollTop = chatWindow.scrollHeight;
            return;
        }

        // --------------------
        // FINAL SOURCE message
        // --------------------
        if (event.data.startsWith("__SOURCE__::")) {
            const source = event.data.replace("__SOURCE__::", "");

            botDiv.innerHTML += `
                <div class="source-box">
                    Source used: <span>${source}</span>
                </div>
            `;

            eventSource.close();
            return;
        }

        // --------------------
        // STREAMED ANSWER TOKENS
        // --------------------
        if (fullAnswer === "") {
            botDiv.innerHTML = "";
        }

        fullAnswer += event.data;
        botDiv.innerHTML = fullAnswer;
        chatWindow.scrollTop = chatWindow.scrollHeight;
    };

    eventSource.onerror = function () {
        eventSource.close();
        botDiv.innerText = "❌ Error streaming response.";
    };
}

// --------------------
// Event Listeners
// --------------------
sendBtn.addEventListener("click", sendQuestion);

userInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        sendQuestion();
    }
});
