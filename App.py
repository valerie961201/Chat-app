from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

data = {"messages": []}
PASSWORD = "letmein"

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat Room</title>
    <script>
        let username = localStorage.getItem('username') || "";
        if (!username) {
            username = prompt("Enter your username:");
            localStorage.setItem('username', username);
        }
        let password = prompt("Enter the chat password:");
        if (password !== "letmein") {
            alert("Incorrect password! Reload to try again.");
            throw new Error("Wrong password");
        }
        async function sendMessage() {
            let msg = document.getElementById("message").value;
            document.getElementById("message").value = "";
            await fetch("/send", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, message: msg })
            });
            loadMessages();
        }
        async function deleteMessage(index) {
            await fetch(`/delete/${index}`, { method: "DELETE" });
            loadMessages();
        }
        async function loadMessages() {
            let res = await fetch("/messages");
            let data = await res.json();
            let chatBox = document.getElementById("chat");
            chatBox.innerHTML = "";
            data.messages.forEach((msg, index) => {
                chatBox.innerHTML += `<div> <b>${msg.username}:</b> ${msg.text} <button onclick="deleteMessage(${index})">❌</button></div>`;
            });
        }
        setInterval(loadMessages, 2000);
    </script>
</head>
<body onload="loadMessages()">
    <h2>Chat Room</h2>
    <div id="chat" style="border:1px solid #ccc; padding:10px; height:300px; overflow:auto;"></div>
    <input type="text" id="message" placeholder="Type your message...">
    <button onclick="sendMessage()">Send</button>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/send', methods=['POST'])
def send_message():
    msg = request.json
    data['messages'].append({"username": msg['username'], "text": msg['message']})
    return jsonify({"status": "Message sent"})

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify({"messages": data['messages']})

@app.route('/delete/<int:index>', methods=['DELETE'])
def delete_message(index):
    if 0 <= index < len(data['messages']):
        del data['messages'][index]
    return jsonify({"status": "Message deleted"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
