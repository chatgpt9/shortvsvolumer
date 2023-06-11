from flask import Flask, request, render_template
import urllib.parse
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    video_url = request.args.get('video')
    if not video_url:
        return 'No video URL provided.'

    # Decode the URL
    video_url = urllib.parse.unquote(video_url)

    # Download the video
    subprocess.call(['youtube-dl', '-o', 'video.mp4', video_url])

    # Crop the video
    subprocess.call(['ffmpeg', '-i', 'video.mp4', '-filter:v', 'crop=iw/2:ih:0:0', 'left.mp4'])
    subprocess.call(['ffmpeg', '-i', 'video.mp4', '-filter:v', 'crop=iw/2:ih:ow:0', 'right.mp4'])

    # Merge the cropped videos
    subprocess.call(['ffmpeg', '-i', 'left.mp4', '-i', 'right.mp4', '-filter_complex', '[0:v][1:v]vstack', 'final.mp4'])

    return 'Video downloaded, cropped, and merged successfully.'

if __name__ == '__main__':
    app.run()
