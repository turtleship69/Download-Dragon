import json
import os
from flask import Flask, request
from pathlib import Path

#set current path to path script is running from 
#print(Path(__file__).parent.resolve())
os.chdir(Path(__file__).parent.resolve())

with open('Download Dragon/config.json', 'r') as f:
    #print(f.read())
    config = json.load(f)



if config['runLocalServer']:
    host = config['serverHost']
    port = config['port']

    app = Flask(__name__)

    os.chdir(str(Path.home() / "Downloads"))

    @app.route('/download', methods=['POST'])
    def download():
        url = request.json['url']
        audio_only = request.json.get('audioOnly', False)

        command = f"yt-dlp --no-mtime --no-colors {url}"

        if audio_only:
            command += ' --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s"'

        print("\033[34m") # set output color to blue
        print(command)
        os.system(command)
        print("\033[0m")

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
