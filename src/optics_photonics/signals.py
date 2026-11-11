"""Local completion and cancellation signals; calculation records remain in SQLite."""
from contextlib import contextmanager
import socket
import threading
import time
import uuid


class Cancellation:
    def __init__(self):
        self.lock = threading.RLock()
        self.cancelled = False
        self.callbacks = set()

    def __call__(self):
        with self.lock:
            return self.cancelled

    def set(self):
        with self.lock:
            self.cancelled = True
            for callback in tuple(self.callbacks):
                callback()

    @contextmanager
    def subscribe(self, callback):
        with self.lock:
            self.callbacks.add(callback)
            if self.cancelled:
                callback()
        try:
            yield
        finally:
            with self.lock:
                self.callbacks.discard(callback)


class Wakeup:
    """One loopback socket per scheduler/reader; subscribe before reading state.

    Datagram contents are ignored. They only wake a reader, which then reads the
    committed state. A bounded wait also recovers from lost local notifications.
    """
    def __init__(self, path):
        from .jobs import database
        self.path, self.key = path, str(uuid.uuid4())
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('127.0.0.1', 0))
        self.port = self.socket.getsockname()[1]
        with database(path) as db:
            db.execute('DELETE FROM wakeups WHERE expires<?', (time.time(),))
            db.execute('INSERT INTO wakeups VALUES(?,?,?)', (self.key, self.port, time.time()+60))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        from .jobs import database
        try:
            with database(self.path) as db:
                db.execute('DELETE FROM wakeups WHERE id=?', (self.key,))
        finally:
            self.socket.close()

    def wait(self, timeout=2):
        from .jobs import database
        with database(self.path) as db:
            db.execute('UPDATE wakeups SET expires=? WHERE id=?', (time.time()+timeout+60, self.key))
        self.socket.settimeout(timeout)
        try:
            self.socket.recv(1)
            self.socket.setblocking(False)
            while True:
                self.socket.recv(1)
        except (TimeoutError, BlockingIOError):
            pass


def notify(path):
    from .jobs import database
    with database(path) as db:
        ports = [row[0] for row in db.execute('SELECT port FROM wakeups WHERE expires>?', (time.time(),))]
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for port in ports:
            try:
                sender.sendto(b'1', ('127.0.0.1', port))
            except OSError:
                pass
