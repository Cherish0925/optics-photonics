"""Temporary directories for cases whose detached workers outlive a calculation."""
from contextlib import contextmanager
import errno
import os
import tempfile
import time


def remove(temporary, timeout=5):
    """Remove a TemporaryDirectory that a detached worker may still be leaving.

    After releasing its run lock a worker notifies readers and closes its
    database, which can add files while the directory is being removed.
    Windows also keeps the worker's inherited log handle until the process exits.
    """
    end = time.monotonic() + timeout
    while True:
        try:
            temporary.cleanup()
            return
        except OSError as exc:
            finishing = exc.errno == errno.ENOTEMPTY or (os.name == 'nt' and isinstance(exc, PermissionError))
            if not finishing or time.monotonic() >= end:
                raise
            time.sleep(.02)


@contextmanager
def workspace(**options):
    """A temporary directory name, removed with remove()."""
    temporary = tempfile.TemporaryDirectory(**options)
    try:
        yield temporary.name
    finally:
        remove(temporary)
