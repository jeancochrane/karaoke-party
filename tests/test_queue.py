from unittest import TestCase

import psycopg2 as pg
import psycopg2.extensions as pg_extensions

import tests.env
import karaoke
from karaoke.queue import Queue
from karaoke.exceptions import QueueError
from tests.conftest import KaraokeTestCase


class TestQueue(KaraokeTestCase):
    '''
    Test some methods of the Queue class.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Set up a test client and database.
        '''
        # Create the test database using an external connection
        cls.ext_conn = karaoke.connect_db()
        cls.ext_conn.set_isolation_level(pg_extensions.ISOLATION_LEVEL_AUTOCOMMIT)

        with cls.ext_conn:
            with cls.ext_conn.cursor() as curs:
                curs.execute('CREATE DATABASE karaoke_test;')

        # Set up the test client
        super().setUpClass()

        # Initialize the test database
        with karaoke.app.app_context():
            karaoke.init_db()

        # Connect to the test database and create a queue to test
        cls.conn = karaoke.connect_db()
        cls.queue = Queue(cls.conn)

        # Load some fake song data
        with cls.conn:
            with cls.conn.cursor() as curs:
                curs.execute('''
                    INSERT INTO song
                        (title, artist, url)
                    VALUES
                        ('foo', 'bar', 'baz')
                    ''')

    @classmethod
    def tearDownClass(cls):
        '''
        Remove the test database and close out the connection.
        '''
        cls.conn.close()

        with cls.ext_conn:
            with cls.ext_conn.cursor() as curs:
                curs.execute('DROP DATABASE karaoke_test')

        # Close out all connections
        cls.ext_conn.close()

    def tearDown(self):
        self.queue.flush()

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

    def test_queue_flush(self):

        singer, song_id = 'foo', 1

        self.queue.add(singer, song_id)

        self.queue.flush()

        # Make sure there's nothing on the queue
        no_singer, no_song_id, no_queue_id = self.queue.get()
        for item in (no_singer, no_song_id, no_queue_id):
            self.assertIsNone(item)
