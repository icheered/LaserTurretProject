"""codeauthor:: Brand Hauser"""

import logging


class Messenger:
    def __init__(self):
        self.message_queue = []

    def send(self, msg):
        self.message_queue.append(msg)

    def get_message(self):
        msg = self.message_queue.pop(0)
        return msg

    def clear_queue(self):
        self.message_queue.clear()

    def is_empty(self):
        return len(self.message_queue) == 0
