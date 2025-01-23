from screenshot_grabber import take_screenshot


def run_pipeline():
    """
    Main function that runs all processing steps in sequence.
    Returns True if successful, False if any step fails.
    """
    try:
        # Step 1: Get reddit post data and screenshot
        from screenshot_grabber import take_screenshot
        take_screenshot()

        # Step 2: Make TTS MP3 file with tik tok or elevenlabs
        from tiktok_TTS import main
        main()

        # Step 3: Create the video combining TTS, MP3 file, and background video
        from video_builder import build_clip, view_file
        build_clip("media/post_screenshot.png", "media/voiceover.mp3", "media/andrew.mp4",
                   "media/final_video.mp4")

        print("All processing completed successfully!")
        return True

    except Exception as error:
        # If anything goes wrong, print the error and return False
        print(f"An error occurred: {str(error)}")
        return False


# This lets you run everything by just running this file
if __name__ == "__main__":
    run_pipeline()
