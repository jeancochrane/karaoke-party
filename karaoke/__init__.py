from flask import Flask, g

app = Flask('karaoke')

from karaoke import routes
