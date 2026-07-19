from flask import Flask, request, jsonify
import yt_dlp
import logging

app = Flask(__name__)

# Configure logging to print to console
logging.basicConfig(level=logging.INFO)

# This will run before every request to log its details
@app.before_request
def log_request_info():
    app.logger.info(f"--- Incoming Request ---")
    app.logger.info(f"URL: {request.url}")
    app.logger.info(f"Method: {request.method}")
    app.logger.info(f"Headers:\n{request.headers}")

@app.route('/', methods=['GET'])
def home():
    return "DramaBox Downloader API is running!"

@app.route('/api/extract', methods=['GET'])
def extract_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "សូមបញ្ចូល URL"}), 400

    # កំណត់ yt-dlp ដើម្បីទាញយកតែ Link MP4 (មិន download ចូល server ទេ)
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url', '')
            title = info.get('title', 'Video')
            
            return jsonify({
                "success": True,
                "title": title,
                "video_url": video_url # នេះជា Link MP4 សុទ្ធដែល Android អាច Download បាន
            })
    except Exception as e:
        app.logger.error(f"Extraction failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)