import sys
from helpers.generic import htmlEsc


def debug(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


class Messages:
    def __init__(self, app):
        self.app = app
        self.messages = []

    def clearMessages(self):
        self.messages.clear()

    def debug(self, msg):
        self._addMessage("debug", msg)

    def info(self, msg):
        self._addMessage("info", msg)

    def warning(self, msg):
        self._addMessage("warning", msg)

    def error(self, msg):
        self._addMessage("error", msg)

    def generateMessages(self):
        html = []

        for (tp, msg) in self.messages:
            html.append(f"""<p class="message {tp}">{htmlEsc(msg)}</p>""")
        self.clearMessages()

        return "\n".join(html)

    def _addMessage(self, tp, msg):
        app = self.app
        debug = app.config["DEBUG"]
        if tp != "debug" or debug:
            self.messages.append((tp, msg))
