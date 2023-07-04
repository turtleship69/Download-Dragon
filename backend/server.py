def download_dragon(background=False):
    import json, os
    from flask import Flask, request
    from pathlib import Path
    from sys import argv, stdout
    import yt_dlp

    # set current path to path script is running from
    os.chdir(Path(__file__).parent.resolve())
    ffmpeg_path = os.path.join(os.path.dirname(__file__), "../backend/ffmpeg/ffmpeg.exe")
    print(__file__)
    print(f"ffmpeg path: {str(ffmpeg_path)}")

    with open(
        os.path.join(os.path.dirname(__file__), "../Download Dragon/config.json"), "r"
    ) as f:
        # print(f.read())
        config = json.load(f)

    if config["runLocalServer"]:
        host = config["serverHost"]
        port = config["port"]

        app = Flask(__name__)

        #     print(str(Path.home() / "Downloads"))
        #     os.chdir(str(Path.home() / "Downloads"))
        # else:
        #     path = argv[2] if len(argv) > 2 else os.path.join(os.environ["PUBLIC"], "Downloads")
        #     print(path)
        #     os.chdir(path)

        os.chdir(config["downloadPath"])

        @app.route("/alive")
        def alive():
            return {"status": "alive"}

        @app.route("/download", methods=["POST"])
        def download():
            if "service_mode" in argv:
                f = open(
                    os.path.join(os.path.dirname(__file__), "../script stdout.txt"), "w"
                )
            else:
                f = stdout

            url = request.json["url"]
            audio_only = request.json.get("audioOnly", False)

            ydl_opts = {
                "final_ext": "mp4",
                "format": "bestvideo+bestaudio[ext=m4a]/best",
                "merge_output_format": "mp4",
                "postprocessors": [
                    {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
                ],
                "updatetime": False,
                "ffmpeg_location": ffmpeg_path,
                'noprogress': True, 
                'quiet': True
            }

            # command = f"\"{Path(__file__).parent.resolve()}\yt-dlp-win\yt-dlp.exe\" --no-mtime --no-colors {url}"
            # print(command, file=f)

            if audio_only:
                # command += ' --extract-audio --audio-format mp3 -o "%(title)s.%(ext)s"'
                ydl_opts = {
                    "final_ext": "mp3",
                    "format": "bestaudio/best",
                    "outtmpl": {"default": "%(title)s.%(ext)s"},
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "nopostoverwrites": False,
                            "preferredcodec": "mp3",
                            "preferredquality": "5",
                        }
                    ],
                    "updatetime": False,
                    "ffmpeg_location": ffmpeg_path,
                'noprogress': True, 
                'quiet': True
                }

            yt_dlp.YoutubeDL(ydl_opts).download([url])

            if "service_mode" in argv:
                f.close()

            return {"status": "success"}

        @app.after_request
        def after_request(response):
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add(
                "Access-Control-Allow-Headers", "Content-Type,Authorization"
            )
            response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE")
            return response

        if __name__ == "__main__" or background:
            app.run(host=host, port=port)  # , debug=True)
            print("hello cruel world")


if __name__ == "__main__":
    download_dragon()
