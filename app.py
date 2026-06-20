from flask import Flask, request, Response, stream_with_context
import subprocess
app = Flask(__name__)
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,OPTIONS"
    return response
@app.route('/stream', methods=['GET'])
def stream_audio():
    youtube_url = request.args.get('url')
    if not youtube_url:
        return {"error": "Missing 'url' parameter"}, 400
    cmd = [
        'yt-dlp',
        '-f', 'bestaudio',
        '-o', '-', 
        youtube_url
    ]
    def generate_chunks():
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        try:
            while True:
                chunk = process.stdout.read(4096)
                if not chunk:
                    break
                yield chunk
        finally:
            process.kill()
    return Response(
        stream_with_context(generate_chunks()), 
        mimetype="audio/mpeg"
    )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
