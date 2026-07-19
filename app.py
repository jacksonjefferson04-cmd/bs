from flask import Flask, request, jsonify
import yt_dlp
import logging

# បើកការបង្ហាញ Log នៅក្នុង Console របស់ Render
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Function នេះនឹងព្រីនរាល់ Request ទាំងអស់ដែលចូលមកកាន់ Server
@app.before_request
def log_request_info():
    logger.info(f"--- Incoming Request ---")
    logger.info(f"URL: {request.url}")
    logger.info(f"Method: {request.method}")

@app.route('/', methods=['GET'])
def home():
    return "DramaBox Downloader API is running!"

@app.route('/api/extract', methods=['GET'])
def extract_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "សូមបញ្ចូល URL"}), 400

    logger.info(f"Extracting video for URL: {url}")

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
            
            logger.info(f"Successfully extracted: {title}")
            
            return jsonify({
                "success": True,
                "title": title,
                "video_url": video_url 
            })
    except Exception as e:
        logger.error(f"Error extracting video: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)