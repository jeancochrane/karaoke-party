import psycopg2

from karaoke import app
from karaoke.exceptions import QueueError

class Queue(object):
    '''
    A queue of songs and singers to be played.
    '''
    def __init__(self):
        '''
        Open up a connection to the queue.
        '''
        db_conn = app.config['DB_CONN']
        self.conn = psycopg2.connect(**DB_CONN)

    def get(self):
        '''
        Return the item on the top of the queue.
        '''
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT
                        singer, song_id, queue_id
                    FROM queue
                    ORDER BY date_added DESC
                    LIMIT 1
                ''')

                res = curs.fetchone()

        if res:
            singer, song_id, queue_id = res[:3]
            return (singer, song_id, queue_id)
        else:
            # Nothing on the queue
            return (None, None, None)

    def delete(self, queue_id):
        '''
        Remove an item from the queue.
        '''
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute('''
                    DELETE FROM queue
                    WHERE queue_id = %s
                    RETURNING queue_id
                ''', queue_id)

                deleted = curs.fetchone()

        if deleted:
            deleted_id = deleted[0]
            return deleted_id
        else:
            raise QueueError('Item with the ID {} was not found on the queue'.format(queue_id))

    def add(self, singer, song_id):
        '''
        Add a song to the queue.
        '''
        return queue_id

    def purge(self):
        '''
        Remove all songs from the queue.
        '''
        return True
