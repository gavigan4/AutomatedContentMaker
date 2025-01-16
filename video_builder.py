import os
from moviepy import *
import subprocess


def build_clip(image_path, audio_path, final_path):
    try:
        # Create and save initial video
        video = ImageClip(image_path).with_duration(
            AudioFileClip(audio_path).duration
        ).with_audio(AudioFileClip(audio_path))

        # Use a temporary output file
        temp_output = "temp_output.mp4"
        video.write_videofile(temp_output, fps=24)
        video.close()

        # Normalize audio
        os.makedirs(os.path.dirname(final_path), exist_ok=True)
        subprocess.run([
            'ffmpeg', '-y', '-i', temp_output,
            '-filter:a', 'loudnorm', '-c:v', 'copy', final_path
        ], check=True)

        # Cleanup and return the final path
        os.remove(temp_output)
        return final_path
    except Exception as e:
        print(f"Error: {e}")
        return None


# Usage example
if __name__ == "__main__":
    # Call the build_clip function
    result = build_clip("media/post_screenshot.png", "media/voiceover.mp3", "media/final_video.mp4")

    if result and os.path.exists(result):
        os.system("open " + result if os.name == 'posix' else "start " + result)


