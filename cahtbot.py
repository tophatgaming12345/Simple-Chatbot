from js import document, window, JSON
import random

chat = document.getElementById("chat")
input_box = document.getElementById("user-input")
send_btn = document.getElementById("send")

def load(key, default):
    data = window.localStorage.getItem(key)
    return JSON.parse(data) if data else default

def save(key, value):
    window.localStorage.setItem(key, JSON.stringify(value))

memory = load("memory", {})
knowledge = load("knowledge", {})
usage = load("usage", {})

def add_message(text, sender):
    div = document.createElement("div")
    div.classList.add("message", sender)
    div.innerText = text
    chat.appendChild(div)
    chat.scrollTop = chat.scrollHeight

def learn_response(text):
    try:
        left, right = text.split("=", 1)
        trigger = left.replace("learn:", "").strip()
        response = right.strip()

        knowledge.setdefault(trigger, [])
        if response not in knowledge[trigger]:
            knowledge[trigger].append(response)
            save("knowledge", knowledge)

        return f"Learned 👍 When someone says '{trigger}', I can say '{response}'"
    except:
        return "Use: learn: trigger = response"

def remember_fact(text):
    if "my name is" in text:
        name = text.split("my name is")[-1].strip()
        memory["name"] = name
        save("memory", memory)
        return f"Nice to meet you, {name} 👋"
    return None

def adaptive_reply(trigger):
    options = knowledge.get(trigger, [])
    if not options:
        return None

    weights = []
    for r in options:
        key = f"{trigger}|{r}"
        weights.append(usage.get(key, 1))

    choice = random.choices(options, weights=weights)[0]
    key = f"{trigger}|{choice}"
    usage[key] = usage.get(key, 1) + 1
    save("usage", usage)
    return choice

def bot_reply(text):
    text = text.lower()

    if text.startswith("learn:"):
        return learn_response(text)

    fact = remember_fact(text)
    if fact:
        return fact

    for trigger in knowledge:
        if trigger in text:
            reply = adaptive_reply(trigger)
            if reply:
                return reply

    if "name" in text and "name" in memory:
        return f"Your name is {memory['name']} 🙂"

    return random.choice([
        "Tell me something new.",
        "You can teach me 👀",
        "Interesting.",
        "I'm learning as we talk."
    ])

def send_message(event=None):
    text = input_box.value
    if not text.strip():
        return

    add_message(text, "user")
    input_box.value = ""

    reply = bot_reply(text)
    add_message(reply, "bot")

send_btn.onclick = send_message
input_box.onkeypress = lambda e: send_message() if e.key == "Enter" else None

add_message("Learning chatbot online 🤖🧠", "bot")
