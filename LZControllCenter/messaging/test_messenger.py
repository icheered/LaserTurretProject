"""codeauthor:: Brand Hauser"""

class Messenger:
    def __init__(self):
        self.message_queue = []

    def send(self, msg):
        self.message_queue.append(msg)

    def get_message(self):
        return self.message_queue.pop()
