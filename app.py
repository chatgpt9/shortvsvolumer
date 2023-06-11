from flask import Flask, request, render_template
import pytube
import moviepy.editor as mp

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['GET'])
def process_video():
    video_url = request.args.get('video')

    # Download the YouTube video using pytube
    youtube = pytube.YouTube(video_url)
    video = youtube.streams.filter(only_video=True).first()
    video_file = f"static/{youtube.video_id}.mp4"
    video.download(output_path="static", filename=youtube.video_id)

    # Crop the video
    video = mp.VideoFileClip(video_file)
    video_width, video_height = video.size
    
    # Crop into two parts from the middle vertical center
    half_width = video_width // 2
    left_part = video.crop(x1=0, y1=0, x2=half_width, y2=video_height)
    right_part = video.crop(x1=half_width, y1=0, x2=video_width, y2=video_height)
    
    # Merge the cropped parts
    final_video = mp.concatenate_videoclips([left_part, right_part])
    
    # Save the final video as a file
    final_video_path = f'static/final_{youtube.video_id}.mp4'
    final_video.write_videofile(final_video_path)

    return render_template('index.html', final_video_path=final_video_path)

if __name__ == '__main__':
    app.run(debug=True)
