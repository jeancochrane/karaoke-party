# routes.py -- routes for the app
import json

from flask import request, render_template, make_response

from karaoke import app, get_db
from karaoke.queue import Queue
from karaoke.exceptions import QueueError


@app.route('/play', methods=['GET'])
def play():
    '''
    Play videos off of a queue.
    '''
    queue = Queue(get_db())
    singer, song_id, queue_id = queue.get()
    song = {'singer': singer, 'id': song_id}

    # Override for dev
    song = {'singer': 'jean', 'id': 't3bjPGUDl1k', 'title': 'Boyish by Japanese Breakfast'}
    return render_template('play.html', song=song)


@app.route('/songs', methods=['GET'])
def songs():
    '''
    Display a list of songs for users to choose from.
    '''
    return render_template('songs.html')

@app.route('/queue', methods=['GET', 'POST'])
def queue():
    '''
    Get and post songs to a queue.
    '''
    queue = Queue(get_db())

    if request.method == 'GET':
        # Get next song from the queue
        singer, song_id, queue_id = queue.get()
        status = 200
        response = {'status': 'fetched next song',
                    'singer': singer,
                    'song_id': song_id,
                    'queue_id': queue_id}

    elif request.method == 'POST':
        # Check if the app is deleting a song that has just been played
        if request.args.get('delete'):
            queue_id = request.args.get('queue_id')

            if queue_id:
                try:
                    deleted_id = queue.delete(queue_id)
                except QueueError:
                    status = 403
                    response = {'status': 'an item was not found on the queue with the id %s' % queue_id}
                else:
                    status = 200
                    response = {'status': 'deleted song with queue id %s' % deleted_id,
                                'queue_id': deleted_id}
            else:
                status = 403
                response = {'status': 'a `delete` request requires an `id` parameter'}
        else:
            # Add song and user data onto the quue
            singer = request.form.get('singer')
            song_id = request.form.get('song_id')

            if singer and song_id:
                queue_id = queue.add(singer, song_id)
                status = 200
                response = {'status': 'added song to queue', 'queue_id': queue_id}
            else:
                status = 403
                response = {'status': 'an `add` request requires form data for a `singer` and `song_id`'}

    return make_response(json.dumps(response), status)
