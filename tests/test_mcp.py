import json
import os
from pathlib import Path
import queue
import subprocess
import sys
import tempfile
import threading
import time
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from optics_photonics import environments, jobs
from optics_photonics.mcp import Connection
from support import remove

SRC = str(Path(__file__).resolve().parents[1] / 'src')
ACTIVE = ('queued', 'running')  # a detached worker may still be starting


class Session:
    """A host connection: requests are written without waiting for earlier replies."""
    def __init__(self, home):
        env = {**os.environ, 'OPTICS_HOME': str(home), 'PYTHONPATH': SRC + os.pathsep + os.environ.get('PYTHONPATH', '')}
        self.process = subprocess.Popen([sys.executable, '-B', '-m', 'optics_photonics', 'mcp'], env=env,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8')
        self.replies = queue.Queue()
        self.reader = threading.Thread(target=self.read, daemon=True)
        self.reader.start()
        self.send({'jsonrpc': '2.0', 'id': 'init', 'method': 'initialize', 'params': {'protocolVersion': '2025-11-25'}})
        self.reply()

    def read(self):
        for line in self.process.stdout:
            self.replies.put((json.loads(line), time.monotonic()))
        self.replies.put((None, time.monotonic()))

    def send(self, message):
        self.process.stdin.write(json.dumps(message) + '\n'); self.process.stdin.flush()

    def call(self, id, name, arguments):
        self.send({'jsonrpc': '2.0', 'id': id, 'method': 'tools/call', 'params': {'name': name, 'arguments': arguments}})

    def reply(self, timeout=20):
        message, at = self.replies.get(timeout=timeout)
        return message, at

    def close(self):
        """End of input, as when a host disconnects; returns the server's exit code."""
        self.process.stdin.close()
        return self.process.wait(timeout=20)

    def release(self):
        if self.process.poll() is None:
            self.process.kill(); self.process.wait()
        self.reader.join(5)  # The reader ends at end of output.
        if not self.process.stdin.closed: self.process.stdin.close()
        self.process.stdout.close()


class ConcurrentRequestsCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name)
        script = self.home / 'slow.py'
        script.write_text('import time\ntime.sleep(60)\n')
        environments.register('slow', 'Slow program', 'Sleeps', kind='command', path=self.home)
        environments.bind('slow', command=[sys.executable, str(script)], path=self.home)
        self.run_id = jobs.submit([{'id': 'sleep', 'tool': 'slow'}], path=self.home)['run_id']
        self.session = Session(self.home)

    def tearDown(self):
        self.session.release()
        jobs.cancel(self.run_id, path=self.home)
        jobs.status(self.run_id, path=self.home, wait=10)
        deadline = time.monotonic() + 10  # until the detached worker releases its run lock
        while time.monotonic() < deadline:
            with jobs.worker_lock(self.home, self.run_id) as free:
                if free: break
            time.sleep(.05)
        remove(self.temp)

    def test_short_requests_are_answered_while_a_status_wait_is_active(self):
        s = self.session
        sent = time.monotonic()
        s.call(1, 'run_status', {'run_id': self.run_id, 'wait': 3})
        s.send({'jsonrpc': '2.0', 'id': 2, 'method': 'ping'})
        s.call(3, 'software_search', {'query': 'thin film', 'limit': 1})
        s.call(4, 'list_runs', {})
        arrived = {}
        for _ in range(3):
            message, at = s.reply()
            arrived[message['id']] = at - sent
        self.assertEqual(set(arrived), {2, 3, 4})  # all three before the waiting request
        self.assertLess(max(arrived.values()), 2.5)
        message, at = s.reply()
        self.assertEqual(message['id'], 1)
        self.assertIn(message['result']['structuredContent']['state'], ACTIVE)
        self.assertGreater(at - sent, 2.5)

    def test_cancel_run_ends_a_concurrent_wait_on_the_same_connection(self):
        s = self.session
        sent = time.monotonic()
        s.call(1, 'run_status', {'run_id': self.run_id, 'wait': 20})
        time.sleep(.3)
        s.call(2, 'cancel_run', {'run_id': self.run_id})
        replies = {}
        for _ in range(2):
            message, at = s.reply()
            replies[message['id']] = (message, at - sent)
        self.assertTrue(replies[2][0]['result']['structuredContent']['cancel_requested'])
        self.assertEqual(replies[1][0]['result']['structuredContent']['state'], 'cancelled')
        self.assertLess(replies[1][1], 10)

    def test_request_cancellation_stops_waiting_without_cancelling_the_calculation(self):
        s = self.session
        sent = time.monotonic()
        s.call(1, 'run_status', {'run_id': self.run_id, 'wait': 20})
        time.sleep(.3)
        s.send({'jsonrpc': '2.0', 'method': 'notifications/cancelled', 'params': {'requestId': 1, 'reason': 'host stopped'}})
        s.send({'jsonrpc': '2.0', 'id': 2, 'method': 'ping'})
        message, _ = s.reply()
        self.assertEqual(message['id'], 2)
        self.assertEqual(s.close(), 0)
        self.assertLess(time.monotonic() - sent, 10)
        message, _ = s.reply()
        self.assertIsNone(message)  # No response to the cancelled request.
        self.assertIn(jobs.status(self.run_id, path=self.home)['state'], ACTIVE)

    def test_closing_the_connection_ends_waits_and_keeps_calculations(self):
        s = self.session
        sent = time.monotonic()
        s.call(1, 'run_status', {'run_id': self.run_id, 'wait': 20})
        time.sleep(.3)
        self.assertEqual(s.close(), 0)
        self.assertLess(time.monotonic() - sent, 10)
        self.assertIn(jobs.status(self.run_id, path=self.home)['state'], ACTIVE)

    def test_many_waits_do_not_occupy_the_workers(self):
        s = self.session
        waits = Connection.WORKERS + 8
        sent = time.monotonic()
        for i in range(waits):
            s.call(f'wait-{i}', 'run_status', {'run_id': self.run_id, 'wait': 4})
        s.call('search', 'software_search', {'query': 'thin film', 'limit': 1})
        s.call('runs', 'list_runs', {})
        first = [s.reply() for _ in range(2)]
        self.assertEqual({message['id'] for message, _ in first}, {'search', 'runs'})
        self.assertLess(max(at for _, at in first) - sent, 3.5)
        s.call('cancel', 'cancel_run', {'run_id': self.run_id})
        rest = [s.reply() for _ in range(waits + 1)]
        self.assertEqual({message['id'] for message, _ in rest}, {'cancel'} | {f'wait-{i}' for i in range(waits)})
        states = {message['result']['structuredContent']['state'] for message, _ in rest if message['id'] != 'cancel'}
        self.assertEqual(states, {'cancelled'})
        self.assertLess(max(at for _, at in rest) - sent, 3.9)  # all waits ended by the cancellation, before 4 s

    def test_invalid_request_ids_are_rejected(self):
        s = self.session
        for bad in (None, True, [1], {'a': 1}, float('inf'), float('nan')):
            s.send({'jsonrpc': '2.0', 'id': bad, 'method': 'ping'})
            message, _ = s.reply()
            self.assertIsNone(message['id'])
            self.assertEqual(message['error']['code'], -32600)
        s.send({'jsonrpc': '2.0', 'method': 'notifications/cancelled', 'params': {'requestId': [1]}})
        s.send({'jsonrpc': '2.0', 'id': 'after', 'method': 'ping'})
        self.assertEqual(s.reply()[0], {'jsonrpc': '2.0', 'id': 'after', 'result': {}})

    def test_repeated_request_id_in_progress_is_rejected(self):
        s = self.session
        s.call(1, 'run_status', {'run_id': self.run_id, 'wait': 3})
        s.call(1, 'list_runs', {})
        message, _ = s.reply()
        self.assertEqual(message['id'], 1)
        self.assertIn('already in progress', message['error']['message'])


if __name__ == '__main__':
    unittest.main()
