from unittest import TestCase

import env
from karaoke.queue import Queue
from karaoke.exceptions import QueueError


class TestQueue(TestCase):
    '''
    Test some methods of the Queue class.
    '''
    def setUp(self):
        self.queue = Queue()

    def tearDown(self):
        self.queue.purge()

    def test_queue_add_and_get(self):

        singer, song_id = 'foo', 1
        queue_id = self.queue.add(singer, song_id)

        queue_attrs = self.queue.get()

        # Make sure the queue returns all of the original information
        for orig, returned in zip(queue_attrs, (singer, song_id, queue_id)):
            self.assertEqual(orig, returned)

    def test_queue_get_empty(self):

        no_singer, no_song_id, no_queue_id = self.queue.get()

        # Make sure there's nothing on the queue
        for item in (no_singer, no_song_id, no_queue_id):
            self.assertIsNone(item)

    def test_queue_delete(self):

        singer, song_id = 'foo', 1
        self.queue.add(singer, song_id)

        got_singer, got_song_id, queue_id = self.queue.get()

        deleted_id = self.queue.delete(queue_id)

        self.assertEqual(queue_id, deleted_id)

        # Make sure there's nothing on the queue
        no_singer, no_song_id, no_queue_id = self.queue.get()
        for item in (no_singer, no_song_id, no_queue_id):
            self.assertIsNone(item)

    def test_queue_delete_raises_error(self):

        # Delete an item that isn't on the queue
        with self.assertRaises(QueueError):
            self.queue.delete(1)

    def test_queue_purge(self):

        singer, song_id = 'foo', 1

        self.queue.add(singer, song_id)

        self.queue.purge()

        # Make sure there's nothing on the queue
        no_singer, no_song_id, no_queue_id = self.queue.get()
        for item in (no_singer, no_song_id, no_queue_id):
            self.assertIsNone(item)
