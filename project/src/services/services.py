#!/usr/bin/python3
import time
from abc import abstractmethod
from queue import Queue
from threading import Condition, Event, Lock, Thread


class Service(Thread):
    def __init__(
        self, group=None, target=None, name=None, args=..., kwargs=None, *, daemon=None
    ):
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._ev_wait_running: Event = Event()
        self._condition: Condition = Condition()
        self._name: str = name
        self._running: bool = False
        self._mutex: Lock = Lock()
        self._in_queue: Queue = Queue(maxsize=1)

    def start(self):
        if not self._running:
            super().start()
            self.wait_running()

    def set_running(self):
        self._running = True
        self._ev_wait_running.set()

    def wait_running(self):
        if not self._running:
            self._ev_wait_running.wait()

    def stop(self):
        self._running = False

    def run(self):
        self.work_thread()

    def get_queue(self):
        return self._in_queue

    @staticmethod
    @abstractmethod
    def work_thread():
        raise NotImplementedError("work_thread must be implemented by subclasses")


service = Service


if __name__ == "__main__":

    class TestService(Service):
        def __init__(
            self,
            group=None,
            target=None,
            name=None,
            args=...,
            kwargs=None,
            *,
            daemon=None,
        ):
            super().__init__(group, target, name, args, kwargs, daemon=daemon)

        def _start(self):
            self.start()

        def work_thread(self):
            self.set_running()

    t = TestService()
    t._start()
    time.sleep(5)
    t.stop()
