from unittest import TestCase

import tests.env
import karaoke

class KaraokeTestCase(TestCase):
    '''
    Create a test client for the app.
    '''
    @classmethod
    def setUpClass(cls):
        '''
        Initialize testing configs and create a test app.
        '''
        karaoke.app.testing = True
        karaoke.app.config.from_object('tests.test_settings')

        # Create a test client
        cls.app = karaoke.app.test_client()

