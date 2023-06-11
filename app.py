import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get YouTube video URL from the form
        youtube_url = request.form['youtube_url']
    try:
        # Download the YouTube video
        video = YouTube(youtube_url)
        video_stream = video.streams.filter(progressive=True, file_extension='mp4').first()
        video_stream.download('./videos', 'original')

        # Crop the video into two parts
        original_path = './videos/original.mp4'
        video_clip = VideoFileClip(original_path)
        video_width = video_clip.size[0]
        half_width = video_width // 2
        left_clip = video_clip.crop(x1=0, y1=0, x2=half_width, y2=video_clip.size[1])
        right_clip = video_clip.crop(x1=half_width, y1=0, x2=video_width, y2=video_clip.size[1])

        # Merge the cropped clips
        final_clip = concatenate_videoclips([left_clip, right_clip], method='compose')

        # Set the output file path
        output_path = './videos/final.mp4'

        # Write the final video to the output file
        final_clip.write_videofile(output_path, codec='libx264')

        # Remove the original and cropped clips
        os.remove(original_path)

        # Render the index page with the final video URL
        return render_template('index.html', video_url=output_path)
    except Exception as e:
        return str(e)
    else:
        return render_template('index.html', video_url=output_path)

if __name__ == '__main__':
    app.run()
