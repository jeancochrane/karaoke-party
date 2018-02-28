from django.shortcuts import render


def play():
    '''
    Play videos off of a queue.
    '''
    pass


def songs():
    '''
    Display a list of songs for users to choose from.
    '''
    pass


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
