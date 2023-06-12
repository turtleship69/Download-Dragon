import json
import os
from flask import Flask, request
from pathlib import Path


with open('./Download Dragon/config.json', 'r') as f:
    #print(f.read())
    config = json.load(f)

os.chdir(str(Path.home() / "Downloads"))

if config['runLocalServer']:
    host = config['serverHost']
    port = config['port']

    app = Flask(__name__)

    @app.route('/download', methods=['POST'])
    def download():
        url = request.json['url']
        audio_only = request.json.get('audioOnly', False)

        command = f"yt-dlp {url}"

        if audio_only:
            command+=" --extract-audio --audio-format mp3"

        print(command)
        os.system(command)

        print("downloaded")

        return {"status": "success"}
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
        return response

    if __name__ == '__main__':
        app.run(host=host, port=port, debug=True)
