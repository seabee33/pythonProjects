# A python script to download a youtube video and convert it from google's shitty vp9 codec to x264

import subprocess, os, glob

url = input("Youtube URL: ")

yt_dlp_command = f'yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best --restrict-filenames" -o "%(title)s.%(ext)s" {url}'
yt_dlp_result = subprocess.run(yt_dlp_command, capture_output=True, text=True, shell=True)

print("yt-dlp output: ", yt_dlp_result.stdout)
print("yt-dlp error: ", yt_dlp_result.stderr)
print("yt-dlp return code: ", yt_dlp_result.returncode)

mp4_files = glob.glob("*.mp4")

if not mp4_files:
    print("No mp4 files found :(")
else:
    downloaded_filename = mp4_files[-1]
    ffmpeg_command = f'ffmpeg -i "{downloaded_filename}" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 192k output.mp4'
    ffmpeg_result = subprocess.run(ffmpeg_command, capture_output=True, text=True, shell=True)

    print("ffmpeg output: ", ffmpeg_result.stdout)
    print("ffmpeg error: ", ffmpeg_result.stderr)
    print("ffmpeg return code: ", ffmpeg_result.returncode)

    os.remove(downloaded_filename)
    print(f"Deleted: {downloaded_filename}")

    os.rename("output.mp4", downloaded_filename)
    print(f"Renamed output.mp4 to {downloaded_filename}")
