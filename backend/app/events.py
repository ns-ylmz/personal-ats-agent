import asyncio

class EventBroadcaster:
    def __init__(self):
        self.listeners = []

    def subscribe(self, loop: asyncio.AbstractEventLoop, q: asyncio.Queue):
        self.listeners.append((loop, q))

    def unsubscribe(self, loop: asyncio.AbstractEventLoop, q: asyncio.Queue):
        if (loop, q) in self.listeners:
            self.listeners.remove((loop, q))

    def broadcast(self, message: dict):
        for loop, q in self.listeners:
            try:
                loop.call_soon_threadsafe(q.put_nowait, message)
            except RuntimeError:
                pass

job_events = EventBroadcaster()
