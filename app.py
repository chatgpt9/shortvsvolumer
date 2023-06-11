import os
import subprocess
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download_video():
    # YouTube video URL
    youtube_url = 'https://www.youtube.com/watch?v=Ip1ne0FwiVU'

    # Download the YouTube video using youtube-dl
    download_command = f'youtube-dl -f mp4 {youtube_url} -o video.mp4'
    subprocess.call(download_command, shell=True)

    # Crop the video
    crop_command = 'ffmpeg -i video.mp4 -filter:v "crop=iw/2:ih:0:0" left.mp4'
    subprocess.call(crop_command, shell=True)
    crop_command = 'ffmpeg -i video.mp4 -filter:v "crop=iw/2:ih:ow/2:0" right.mp4'
    subprocess.call(crop_command, shell=True)

    # Merge the cropped videos
    merge_command = 'ffmpeg -i left.mp4 -i right.mp4 -filter_complex "vstack" final.mp4'
    subprocess.call(merge_command, shell=True)

    # Remove the temporary files
    os.remove('video.mp4')
    os.remove('left.mp4')
    os.remove('right.mp4')

    return 'Video downloaded and processed successfully.'

if __name__ == '__main__':
    app.run()
