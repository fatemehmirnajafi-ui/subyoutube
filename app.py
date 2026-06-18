from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube Transcript API is running. Use /transcript?video_id=YOUR_VIDEO_ID"

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    
    if not video_id:
        return jsonify({'error': 'Video ID is missing.'}), 400

    try:
        # دریافت زیرنویس (اولویت با انگلیسی و سپس فارسی)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'fa'])
        
        # چسباندن تمام جملات به یکدیگر برای ارسال به هوش مصنوعی
        full_text = " ".join([t['text'] for t in transcript_list])
        
        return jsonify({
            'status': 'success',
            'video_id': video_id,
            'transcript': full_text
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'error_message': str(e)
        }), 500

if __name__ == '__main__':
    # این تنظیمات برای اجرای روی سرور Render ضروری است
    app.run(host='0.0.0.0', port=10000)