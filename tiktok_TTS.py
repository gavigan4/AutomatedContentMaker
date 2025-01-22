import requests, base64, random, argparse, os, playsound, sys, time, re, textwrap, json
from constants import voices

API_BASE_URL = f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/"
USER_AGENT = f"com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; " \
             f"Build/NRD90M;tt-ok/3.12.13.1)"


# reading text to be read
def load_text_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    print(json.dumps(data, indent=4))  # Pretty print as text
    combined_text = f"{data['title']}\n\n{data['content']}"
    return combined_text


def split_text_into_chunks(text, chunk_size=200):
    """
       Split text into chunks of a given size while preserving whole sentences
       and ensuring each chunk is less than the chunk size.
    """
    # Get rid of all *s
    text.replace("*", "")

    # Split text into sentences using punctuation marks as delimiters
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= chunk_size:  # +1 for space
            # Add sentence to the current chunk
            if current_chunk:
                current_chunk += " "
            current_chunk += sentence
        else:
            # Save the current chunk and start a new one
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def delete_chunk_files(output_dir):
    """
        Deletes all chunk files from the specified directory.
        """
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.startswith("chunk_") and file.endswith(".mp3"):
                os.remove(os.path.join(root, file))
                print(f"Deleted: {os.path.join(root, file)}")


# Default settings - modify these values
DEFAULT_SESSION_ID = "4c9e249999d6abb3ee7e079ad719bea4"  # Replace with your session ID
DEFAULT_VOICE = "en_uk_003"
DEFAULT_TEXT = load_text_from_json('media/temp_post_data.json')
DEFAULT_OUTPUT_FILE = "voice.mp3"
DEFAULT_PLAY_SOUND = False


def tts(session_id: str, text_speaker: str = "es_mx_002", req_text: str = "TikTok Text To Speech",
        filename: str = 'voice.mp3', play: bool = False):
    req_text = req_text.replace("+", "plus")
    req_text = req_text.replace(" ", "+")
    req_text = req_text.replace("&", "and")
    req_text = req_text.replace("ä", "ae")
    req_text = req_text.replace("ö", "oe")
    req_text = req_text.replace("ü", "ue")
    req_text = req_text.replace("ß", "ss")

    r = requests.post(
        f"{API_BASE_URL}?text_speaker={text_speaker}&req_text={req_text}&speaker_map_type=0&aid=1233",
        headers={
            'User-Agent': USER_AGENT,
            'Cookie': f'sessionid={session_id}'
        }
    )

    # debug print
    print("API Response:", r.text)

    if r.json()["message"] == "Couldn't load speech. Try again.":
        output_data = {"status": "Session ID is invalid", "status_code": 5}
        print(output_data)
        return output_data

    vstr = [r.json()["data"]["v_str"]][0]
    msg = [r.json()["message"]][0]
    scode = [r.json()["status_code"]][0]
    log = [r.json()["extra"]["log_id"]][0]

    dur = [r.json()["data"]["duration"]][0]
    spkr = [r.json()["data"]["speaker"]][0]

    b64d = base64.b64decode(vstr)

    with open(filename, "wb") as out:
        out.write(b64d)

    output_data = {
        "status": msg.capitalize(),
        "status_code": scode,
        "duration": dur,
        "speaker": spkr,
        "log": log
    }

    print(output_data)

    if play is True:
        playsound.playsound(filename)
        os.remove(filename)

    return output_data


def tts_with_split(session_id, text_speaker, req_text, output_dir="media", play=False):
    """
     tts when text has >200 characters
    """
    text_chunks = split_text_into_chunks(req_text, chunk_size=200)
    output_files = []

    for idx, chunk in enumerate(text_chunks):
        filename = os.path.join(output_dir, f"chunk_{idx}.mp3")
        print(f"Processing chunk {idx + 1}/{len(text_chunks)}: {chunk}")
        response = tts(session_id, text_speaker, chunk, filename, play=False)

        # if the tik tok tts goes well for a chunk
        if response.get("status_code") == 0:
            output_files.append(filename)
            print(f"Success processing chunk {idx + 1}: {response}")
        else:
            print(f"Error processing chunk {idx + 1}: {response}")

    # Combine audio files
    combined_filename = os.path.join(output_dir, "combined_output.mp3")
    with open(combined_filename, 'wb') as combined_file:
        for file in output_files:
            with open(file, 'rb') as f:
                combined_file.write(f.read())

    if play:
        playsound.playsound(combined_filename)

    # delete leftover chunk files
    delete_chunk_files(output_dir)

    print(f"Combined audio saved to: {combined_filename}")
    return combined_filename


def main():
    """Function to run TTS with default settings"""
    print(f"Running TTS with default settings:")
    print(f"Voice: {DEFAULT_VOICE}")
    print(f"Text: {DEFAULT_TEXT}")
    print(f"Output file: {DEFAULT_OUTPUT_FILE}")

    return tts_with_split(
        session_id=DEFAULT_SESSION_ID,
        text_speaker=DEFAULT_VOICE,
        req_text=DEFAULT_TEXT,
        play=DEFAULT_PLAY_SOUND
    )


# for merging multiple mp3s
def batch_create(filename: str = 'voice.mp3'):
    out = open(filename, 'wb')

    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
        return sorted(data, key=alphanum_key)

    for item in sorted_alphanumeric(os.listdir('./batch/')):
        filestuff = open('./batch/' + item, 'rb').read()
        out.write(filestuff)

    out.close()


if __name__ == "__main__":
    main()
    # # print(DEFAULT_TEXT)
    # print(len(split_text_into_chunks(DEFAULT_TEXT)))
