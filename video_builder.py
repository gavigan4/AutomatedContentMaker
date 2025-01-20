import os
import subprocess
from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
import platform


def build_clip(image_path, audio_path, gameplay_path, final_path):
    try:
        # Load the gameplay background video
        gameplay_clip = VideoFileClip(gameplay_path).without_audio()

        # Create an ImageClip and add audio to it
        audio_clip = AudioFileClip(audio_path)
        image_clip = ImageClip(image_path).with_duration(audio_clip.duration).with_audio(audio_clip)

        # Position the image clip at the upper center 100 pixels from top
        image_clip = image_clip.with_position(lambda t: ("center", 100))

        # Create a composite video with the gameplay and image clip
        composite_clip = CompositeVideoClip([gameplay_clip, image_clip])
        composite_clip = composite_clip.with_duration(min(gameplay_clip.duration, image_clip.duration))

        # Use a temporary output file for the composite video
        temp_output = "temp_output.mp4"
        composite_clip.write_videofile(temp_output, fps=24)

        # cropping the composite video to correct aspect ratio

        # Normalize audio in the final output
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        subprocess.run([
            'ffmpeg', '-y', '-i', temp_output,
            '-filter:a', 'loudnorm', '-c:v', 'copy', final_path
        ], check=True)

        # Cleanup temporary files
        gameplay_clip.close()
        image_clip.close()
        audio_clip.close()
        composite_clip.close()
        os.remove(temp_output)

        # data on final video
        print("width: " + composite_clip.w)
        print("height: " + composite_clip.h)

        return final_path
    except Exception as e:
        print(f"Error: {e}")
        return None


def view_file(file_path):
    if platform.system() == "Windows":
        os.startfile(file_path)
    elif platform.system() == "Darwin":  # macOS
        os.system(f"open {file_path}")
    else:  # Linux
        os.system(f"xdg-open {file_path}")


if __name__ == "__main__":
    build_clip("media/post_screenshot.png", "media/voiceover.mp3", "media/gameplay_video.mp4", "media/final_video.mp4")
    view_file("media/final_video.mp4")
