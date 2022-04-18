from typing import Iterable
from .protocol.pipeline import OpenMessage


class Pipeline:

    def __init__(self, source, destination):
        self.source = source()
        self.destination = destination()

    def execute(self):
        messages: Iterable[OpenMessage] = self.source.read()
        self.destination.write(messages)
