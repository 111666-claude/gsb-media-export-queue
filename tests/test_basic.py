import unittest

from export_queue import ExportQueue


class ExportQueueBasicTests(unittest.TestCase):
    def test_one_ready_job(self):
        q = ExportQueue()
        q.apply({"op": "submit", "id": "clip-a", "revision": 1, "ready": 0, "cost": 1, "priority": 5})
        self.assertEqual(q.plan(0, 1), ["clip-a"])


if __name__ == "__main__":
    unittest.main()
