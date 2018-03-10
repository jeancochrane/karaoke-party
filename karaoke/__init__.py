import psycopg2 as pg
import psycopg2.sql as sql
from flask import Flask, g

# Create an instance of the app
app = Flask('karaoke')

# Register configs
app.config.from_object('karaoke.settings')

# Import the routes
from karaoke import routes

# Database methods

def connect_db():
    '''
    Create a connection to the database.
    '''
    CONN_OPTS = app.config['DB_CONN']
    db_conn = pg.connect(**CONN_OPTS)
    return db_conn

def get_db():
    '''
    Retrieve a connection to the database and scope it to the application context, or
    create one if it doesn't exist.
    '''
    if not hasattr(g, 'db_conn'):
        g.db_conn = connect_db()
    return g.db_conn

@app.teardown_appcontext
def disconnect_db(error):
    '''
    Disconnect the database connection scoped to the application context.
    '''
    if hasattr(g, 'db_conn'):
        g.db_conn.close()

def init_db():
    '''
    Create the table schema for this app.
    '''
    drop_table = '''
        DROP TABLE IF EXISTS {} CASCADE
    '''

    create_songs = '''
        CREATE TABLE song (
            id           SERIAL PRIMARY KEY,
            title        VARCHAR(250) NOT NULL,
            artist       VARCHAR(100) NOT NULL,
            release_date DATE,
            url          VARCHAR(250) NOT NULL
        )
    '''

    create_queue = '''
        CREATE TABLE queue (
            id         SERIAL PRIMARY KEY,
            singer     VARCHAR(100) NOT NULL,
            date_added TIMESTAMP DEFAULT current_timestamp,
            song_id    INTEGER NOT NULL REFERENCES song(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    '''

    conn = get_db()

    with conn:
        with conn.cursor() as curs:
            curs.execute(sql.SQL(drop_table).format(sql.Identifier('song')))
            curs.execute(sql.SQL(drop_table).format(sql.Identifier('queue')))
            curs.execute(create_songs)
            curs.execute(create_queue)

            # Add constraints
            curs.execute('''
                ALTER TABLE queue
                ADD CONSTRAINT song_fk
                FOREIGN KEY (song_id)
                REFERENCES song (id)
                ON DELETE CASCADE
            ''')

    conn.close()

@app.cli.command('initdb')
def initdb_command():
    '''
    Shell command for initializing the database.
    '''
    init_db()
    print('Initialized the database')
