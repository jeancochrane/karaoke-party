from unittest import TestCase

import env
import karaoke


class TestRoutes(TestCase):
    '''
    Test the API routes.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Set up some class-wide attributes for testing.
        '''
        karaoke.app.testing = True
        cls.app = karaoke.app.test_client()

    def assertResponseEqual(self, condition, response):
        '''
        Helper method that wraps `self.assertEqual()` and provides more exception
        context.
        '''
        try:
            self.assertEqual(*condition)
        except AssertionError as e:
            print(response.data.decode('utf-8'))
            raise e

    def test_play_resolves(self):
        get_request = self.app.get('/play')
        self.assertResponseEqual((get_request.status_code, 200), response=get_request)

    def test_songs_resolves(self):
        get_request = self.app.get('/songs')
        self.assertResponseEqual((get_request.status_code, 200), response=get_request)

    def test_add_to_queue(self):

        post_data = {
            'singer': 'foo',
            'song_id': '1',
        }

        post_request = self.app.post('/queue', data=post_data)
        self.assertResponseEqual((post_request.status_code, 200), response=post_request)

        json_response = json.loads(post_request.data.decode('utf-8'))
        self.assertEqual(json_response.get('queue_id'), '1')

    def test_get_from_queue(self):

        post_data = {
            'singer': 'foo',
            'song_id': '1',
        }

        post_request = self.app.post('/queue', data=post_data)

        get_request = self.app.get('/queue')
        self.assertResponseEqual((get_request.status_code, 200), response=get_request)

        json_response = json.loads(get_request.data.decode('utf-8'))

        self.assertEqual(json_response.get('singer'), post_data['singer'])
        self.assertEqual(json_response.get('song_id'), post_data['song_id'])
        self.assertEqual(json_response.get('queue_id'), '1')

    def test_delete_from_queue(self):

        post_data = {
            'singer': 'foo',
            'song_id': '1',
        }

        post_request = self.app.post('/queue', data=post_data)
        json_response = json.loads(post_request.data.decode('utf-8'))

        queue_id = json_response.get('queue_id')

        delete_request = self.app.post('/queue?delete=true&queue_id=' + queue_id)
        self.assertResponseEqual((delete_request.status_code, 200), response=delete_request)

        delete_response = json.loads(delete_request.data.decode('utf-8'))
        self.assertEqual(delete_response['queue_id'], queue_id)

    def test_queue_delete_missing_id(self):
        # Test a missing id parameter for deletion
        missing_id = self.app.post('/queue?delete=true')
        self.assertResponseEqual((missing_id.status_code, 403), response=missing_id)

        missing_id_response = json.loads(missing_id.data.decode('utf-8'))
        self.assertEqual(missing_id_response.get('status'),
                         'a `delete` request requires an `id` parameter')

    def test_queue_add_missing_singer(self):
        # Test missing singer form data
        missing_singer_data = {'song_id': '1'}
        missing_singer = self.app.post('/queue', data=missing_singer_data)
        self.assertResponseEqual((missing_singer.status_code, 403), response=missing_singer)

        missing_singer_response = json.loads(missing_singer.data.decode('utf-8'))
        self.assertEqual(missing_singer_response.get('status'),
                         'an `add` request requires form data for a `singer` and `song_id`')

    def test_queue_add_missing_song(self):
        # Test missing song_id form data
        missing_song_data = {'singer': 'foo'}
        missing_song = self.app.post('/queue', data=missing_song_data)

        self.assertResponseEqual((missing_song.status_code, 403), response=missing_song)

        missing_song_response = json.loads(missing_song.data.decode('utf-8'))
        self.assertEqual(missing_song_response.get('status'),
                         'an `add` request requires form data for a `singer` and `song_id`')

    def test_queue_delete_queue_id_doesnt_exist(self):
        # Test a delete request for a song that doesn't exist
        bad_queue_id = self.app.post('/queue?delete=true&queue_id=-1')
        self.assertResponseEqual((bad_queue_id.status_code, 403), response=bad_queue_id)

        bad_queue_id_response = json.loads(bad_queue_id.data.decode('utf-8'))
        self.assertEqual(bad_queue_id_response.get('status'),
                         'an item was not found on the queue with the id -1')
