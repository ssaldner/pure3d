class Messages:
    def __init__(self, app):
        self.app = app
        self.messages = []

    def clearMessages(self):
        self.messages.clear()

    def addMessage(self, tp, msg):
        app = self.app
        debug = app.config["DEBUG"]
        if tp != "debug" or debug:
            self.messages.append((tp, msg))

    def generateMessages(self):
        html = []

        for (tp, msg) in self.messages:
            html.append(f"""<p class="message {tp}">{msg}</p>""")
        self.clearMessages()

        return "\n".join(html)
