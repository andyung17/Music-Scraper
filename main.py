from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import jsonify, request
import asyncio
import script

app = Flask(__name__)
api = Api(app)
loop = asyncio.get_event_loop()

@app.route('/song')
def get():
    songRequest = request.args.get('songname')
    test = loop.run_until_complete(script.pyppeteer_test((songRequest)))
    test = loop.run_until_complete(script.get_song_data(test))
    return {'data': test}, 200

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)