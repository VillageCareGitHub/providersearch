from flask import Flask
from flask_cors import CORS

app=Flask(__name__)
cors=CORS(app)

from flask_app import provider_directory_api