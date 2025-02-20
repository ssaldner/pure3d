import sys
from helpers.generic import htmlEsc


def error(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


def info(msg):
    sys.stout.write(f"{msg}\n")
    sys.stout.flush()


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
        html = ["""<div class="messages">"""]

        for (tp, msg) in self.messages:
            html.append(f"""<div class="msgitem {tp}">{htmlEsc(msg)}</div>""")

        html.append("</div>")
        self.clearMessages()
        return "\n".join(html)

    def _addMessage(self, tp, msg):
        app = self.app
        debug = app.config["DEBUG"]
        if tp != "debug" or debug:
            self.messages.append((tp, msg))
