# routes.py -- routes for the app
from flask import request, make_response, g

from karaoke import app


@app.route('/play', methods=['GET'])
def play():
    '''
    Play videos off of a queue.
    '''
    pass


@app.route('/songs', methods=['GET'])
def songs():
    '''
    Display a list of songs for users to choose from.
    '''
    pass

@app.route('/queue', methods=['GET', 'POST'])
def queue():
    '''
    Get and post songs to a queue.
    '''
    if request.method == 'GET':
        # Get songs from the queue
        pass

    elif request.method == 'POST':
        # Add song and user onto the quue
        pass
