import sys
import os
import yt_dlp
from pydub import AudioSegment

# ---------------------------
# Download Videos
# ---------------------------
def download_videos(singer, num_videos):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'noplaylist': True
    }

    search_query = f"ytsearch{num_videos}:{singer}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query])


# ---------------------------
# Convert & Trim Audio
# ---------------------------
def convert_and_trim(duration):
    trimmed_files = []

    for file in os.listdir("downloads"):
        if file.endswith((".mp3", ".m4a", ".webm")):
            path = os.path.join("downloads", file)

            audio = AudioSegment.from_file(path)
            trimmed = audio[:duration * 1000]

            output_path = path.rsplit(".", 1)[0] + ".mp3"
            trimmed.export(output_path, format="mp3")

            trimmed_files.append(output_path)

    return trimmed_files


# ---------------------------
# Merge Audio Files
# ---------------------------
def merge_audios(files, output_name):
    combined = AudioSegment.empty()

    for file in files:
        audio = AudioSegment.from_mp3(file)
        combined += audio

    combined.export(output_name, format="mp3")


# ---------------------------
# Main
# ---------------------------
def main():

    if len(sys.argv) != 5:
        print("Usage: python 102303532.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = sys.argv[1]
    num_videos = int(sys.argv[2])
    duration = int(sys.argv[3])
    output_name = sys.argv[4]

    if num_videos <= 10:
        print("Error: Number of videos must be greater than 10")
        sys.exit(1)

    if duration <= 20:
        print("Error: Duration must be greater than 20 seconds")
        sys.exit(1)

    try:
        download_videos(singer, num_videos)
        files = convert_and_trim(duration)
        merge_audios(files, output_name)

        print("Mashup created successfully!")
        print("Output file:", output_name)

    except Exception as e:
        print("Exception occurred:", e)


if __name__ == "__main__":
    main()
