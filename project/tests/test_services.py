import time

from services.services import Service


class FakeService(Service):
    def work_thread(self):
        self.set_running()
        while self._running:
            time.sleep(0.001)


def test_service_start_stop_and_queue():
    service = FakeService()

    service.start()
    assert service._running is True
    assert service.get_queue().empty()

    service.stop()
    service.join(timeout=1)

    assert service._running is False
    assert not service.is_alive()


def test_wait_running_returns_when_already_running():
    service = FakeService()
    service.set_running()

    service.wait_running()

    assert service._running is True
