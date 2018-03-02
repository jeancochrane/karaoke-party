from flask import Flask, g

app = Flask('karaoke')

from api import routes
