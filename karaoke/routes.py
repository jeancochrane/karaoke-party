# routes.py -- routes for the app
from flask import request, render_template, make_response

from karaoke import app
from karaoke.queue import Queue


@app.route('/play', methods=['GET'])
def play():
    '''
    Play videos off of a queue.
    '''
    return render_template('play.html')


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
    queue = Queue()

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
                    queue.delete(queue_id)
                except QueueDeletionError:
                    status = 403
                    response = {'status': 'an item was not found on the queue with the id %s' % queue_id}
                else:
                    status = 200
                    response = {'status': 'deleted song with queue id %s' % queue_id,
                                'queue_id': queue_id}
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
