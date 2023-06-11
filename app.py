from flask import Flask, request, render_template
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video')
def process_video():
    video_url = request.args.get('video')
    if video_url:
        # Decode the URL
        decoded_url = video_url.replace('%3A', ':').replace('%2F', '/')

        # Download the video
        video_path = download_video(decoded_url)

        # Crop the video
        cropped_video = crop_video(video_path)

        # Merge the cropped parts
        merged_video = merge_videos(cropped_video)

        # Delete the temporary files
        os.remove(video_path)
        os.remove(cropped_video[0])
        os.remove(cropped_video[1])

        return render_template('video.html', video_path=merged_video)
    else:
        return 'Please provide a valid YouTube video URL.'

def download_video(url):
    # Use your preferred method to download the video
    # and return the path to the downloaded video file
    # For simplicity, let's assume it's already downloaded and return the path directly
    return '/path/to/downloaded_video.mp4'

def crop_video(video_path):
    video = VideoFileClip(video_path)

    # Get the middle vertical center position
    mid_y = video.size[1] / 2

    # Crop left part
    left_cropped = video.crop(x1=0, y1=0, x2=video.size[0] / 2, y2=mid_y)
    left_cropped_path = '/path/to/left_cropped.mp4'
    left_cropped.write_videofile(left_cropped_path)

    # Crop right part
    right_cropped = video.crop(x1=video.size[0] / 2, y1=0, x2=video.size[0], y2=mid_y)
    right_cropped_path = '/path/to/right_cropped.mp4'
    right_cropped.write_videofile(right_cropped_path)

    return left_cropped_path, right_cropped_path

def merge_videos(cropped_videos):
    left_video = VideoFileClip(cropped_videos[0])
    right_video = VideoFileClip(cropped_videos[1])

    # Stack the videos vertically
    merged_video = concatenate_videoclips([left_video.set_position("top"), right_video.set_position("top")])

    # Write the merged video to a file
    merged_video_path = '/path/to/merged_video.mp4'
    merged_video.write_videofile(merged_video_path)

    return merged_video_path

if __name__ == '__main__':
    app.run(debug=True)
