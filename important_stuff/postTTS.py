import json
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play, save

# loading env variables
load_dotenv()

json_file = "../post_data.json"

client = ElevenLabs(
    api_key=os.getenv('ELEVEN_LABS_KEY')
)


# Load the text content from the JSON file
def load_text_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    title = data['title']
    content = data['content']
    return title, content


# Generate audio from text
def generate_audio(text, voice="Josh", model="eleven_multilingual_v2"):
    audio = client.generate(
        text=text,
        voice=voice,
        model=model
    )
    return audio


# Main function to run the TTS process
def text_to_speech_from_json(json_file):
    # Load text from the JSON file
    title, content = load_text_from_json(json_file)

    # Combine title and content for TTS
    full_text = f"Title: {title}. Content: {content}"

    # Generate audio using ElevenLabs TTS
    audio = generate_audio(full_text)

    # Play the audio or save it to a file
    # play(audio)  # To play the generated audio
    save(audio, "../output.mp3")  # To save the audio as an MP3 file


# Example usage
if __name__ == "__main__":
    text_to_speech_from_json('../post_data.json')
