from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "DramaBox Downloader API is running!"

@app.route('/api/extract', methods=['GET'])
def extract_video():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "សូមបញ្ចូល URL"}), 400

    # កំណត់ yt-dlp និងបន្ថែម Headers ដើម្បីបន្លំជា Browser ពិតប្រាកដ
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.dramaboxdb.com/',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # ស្វែងរក URL វីដេអូ
            video_url = info.get('url', '')
            if not video_url and 'formats' in info:
                for f in reversed(info['formats']):
                    if f.get('url') and 'manifest' not in f.get('url'):
                        video_url = f['url']
                        break

            title = info.get('title', 'Video')
            
            if video_url:
                return jsonify({
                    "success": True,
                    "title": title,
                    "video_url": video_url
                })
            else:
                return jsonify({"success": False, "error": "រកមិនឃើញ Link MP4 ទេ"}), 404
                
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)