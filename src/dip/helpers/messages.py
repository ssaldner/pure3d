class Messages:
    def __init__(self):
        self.messages = []

    def clearMessages(self):
        self.messages.clear()

    def addMessage(self, tp, msg):
        self.messages.append((tp, msg))

    def generateMessages(self):
        html = []

        for (tp, msg) in self.messages:
            html.append(f"""<p class="message {tp}">{msg}</p>""")
        self.clearMessages()

        return "\n".join(html)
