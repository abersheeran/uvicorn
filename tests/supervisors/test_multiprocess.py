from __future__ import annotations

import socket
import threading
import time

from uvicorn import Config
from uvicorn._types import ASGIReceiveCallable, ASGISendCallable, Scope
from uvicorn.supervisors import Multiprocess


async def app(scope: Scope, receive: ASGIReceiveCallable, send: ASGISendCallable) -> None:
    pass  # pragma: no cover


def run(sockets: list[socket.socket] | None) -> None:
    while True:
        time.sleep(1)


def stop_run(stop) -> None:
    while True:
        time.sleep(1)
        stop()


def test_multiprocess_run() -> None:
    """
    A basic sanity check.

    Simply run the supervisor against a no-op server, and signal for it to
    quit immediately.
    """
    config = Config(app=app, workers=2)
    supervisor = Multiprocess(config, target=run, sockets=[])
    threading.Thread(target=stop_run, args=(supervisor.handle_int,), daemon=True).start()
    supervisor.run()


def test_multiprocess_health_check() -> None:
    """
    Ensure that the health check works as expected.
    """
    config = Config(app=app, workers=2)
    supervisor = Multiprocess(config, target=run, sockets=[])
    threading.Thread(target=supervisor.run, daemon=True).start()
    time.sleep(1)
    process = supervisor.processes[0]
    process.kill()
    assert not process.is_alive()
    time.sleep(1)
    for p in supervisor.processes:
        assert p.is_alive()

    supervisor.handle_int()
