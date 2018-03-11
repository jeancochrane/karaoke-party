import psycopg2

from karaoke.exceptions import QueueError

class Queue(object):
    '''
    A queue of songs and singers to be played.
    '''
    def __init__(self, db_conn=None):
        '''
        Open up a connection to the queue. `db_conn` should be a DBAPI connection
        object.
        '''
        self.conn = db_conn

    def get(self):
        '''
        Return the item on the top of the queue.
        '''
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute('''
                    SELECT
                        singer, song_id, id
                    FROM queue
                    ORDER BY date_added DESC
                    LIMIT 1
                ''')

                res = curs.fetchone()

        if res:
            return res
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
                    WHERE id = %s
                    RETURNING id
                ''', (queue_id,))

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
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute('''
                    INSERT INTO queue
                        (singer, song_id)
                    VALUES
                        (%s, %s)
                    RETURNING id
                    ''', (singer, song_id))

                queue_id = curs.fetchone()[0]

        return queue_id

    def flush(self):
        '''
        Remove all songs from the queue.
        '''
        with self.conn:
            with self.conn.cursor() as curs:
                curs.execute('''
                    TRUNCATE queue
                ''')

        return True
