from flask import Flask, request, Response
import subprocess, os

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.route("/")
def stream():
    url = request.args.get("url")
    if not url:
        return "Use ?url=YOUTUBE_URL"

    def generate():
        p = subprocess.Popen(
            [
                "yt-dlp",
                "-f", "bestaudio",
                "-o", "-",
                "--extract-audio",
                "--audio-format", "mp3",
                url
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        while True:
            data = p.stdout.read(4096)
            if not data:
                break
            yield data

    return Response(
        generate(),
        mimetype="audio/mpeg",
        headers={"Content-Disposition": "inline"}
    )

app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
