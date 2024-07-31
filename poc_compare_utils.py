import pytube
import yt_dlp
import os
import subprocess

def get_incremental_folder_name(base_name):
    """
    Generate an incremental folder name based on the base_name.
    """
    counter = 1
    while True:
        folder_name = f"{base_name} {counter}"
        if not os.path.exists(folder_name):
            return folder_name
        counter += 1

def download_youtube_video_pytube(video_url, base_output_folder):
    # Generate an incremental folder name
    output_folder = get_incremental_folder_name(base_output_folder)
    
    # Ensure the output folder exists
    os.makedirs(output_folder)
    
    # Create a YouTube object with the video URL
    yt = pytube.YouTube(video_url)
    
    # Get the highest resolution progressive stream (video + audio)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    # Define the output file path
    video_path = os.path.join(output_folder, 'video.mp4')
    
    # Download the video stream
    stream.download(filename=video_path)
    print(f"Video downloaded: {stream.title} to {video_path}")

    return output_folder

def download_youtube_video_ytdlp(video_url, base_output_folder):
    # Generate an incremental folder name
    output_folder = get_incremental_folder_name(base_output_folder)
    
    # Ensure the output folder exists
    os.makedirs(output_folder)
    
    # Define options for best quality video download
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': os.path.join(output_folder, 'video.%(ext)s')
    }

    # Download best quality video with audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print(f"Video downloaded to {os.path.join(output_folder, 'video.mp4')}")
        
    return output_folder

def split_youtube_video_pytube(video_url, base_output_folder):
    # Generate an incremental folder name
    output_folder = get_incremental_folder_name(base_output_folder)
    
    # Ensure the output folder exists
    os.makedirs(output_folder)
    
    # Create a YouTube object with the video URL
    yt = pytube.YouTube(video_url)
    
    # Get the highest resolution video stream
    video_stream = yt.streams.filter(progressive=False, file_extension='mp4').order_by('resolution').desc().first()
    
    # Get the highest quality audio stream
    audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').order_by('abr').desc().first()
    
    # Define the output file paths
    video_path = os.path.join(output_folder, 'video.mp4')
    audio_path = os.path.join(output_folder, 'audio.mp4')
    
    #converted mp3 file path
    mp3_path = os.path.join(output_folder, 'audio.mp3')
    
    # Download the video stream
    video_stream.download(filename=video_path)
    print(f"Video downloaded: {video_stream.title} to {video_path}")
    
    # Download the audio stream
    audio_stream.download(filename=audio_path)
    print(f"Audio downloaded: {audio_stream.title} to {audio_path}")
    
    # Convert the audio to MP3 using FFmpeg
    command = [
        'ffmpeg',
        '-i', audio_path,
        '-q:a', '0',
        mp3_path
    ]
    
    subprocess.run(command)
    print(f"Audio converted to MP3: {mp3_path}")

    return output_folder

def split_youtube_video_ytdlp(video_url, base_output_folder):
    # Generate an incremental folder name
    output_folder = get_incremental_folder_name(base_output_folder)
    
    # Ensure the output folder exists
    os.makedirs(output_folder)
    
    # Define options for video download
    ydl_opts_video = {
        'format': 'bestvideo[ext=mp4]',
        'outtmpl': os.path.join(output_folder, 'video.%(ext)s')
    }
    
    # Define options for audio download and conversion to mp3
    ydl_opts_audio = {
        'format': 'bestaudio',
        'outtmpl': os.path.join(output_folder, 'audio.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    # Download video
    with yt_dlp.YoutubeDL(ydl_opts_video) as ydl:
        ydl.download([video_url])
        print(f"Video downloaded to {os.path.join(output_folder, 'video.mp4')}")
    
    # Download audio
    with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
        ydl.download([video_url])
        print(f"Audio downloaded and converted to MP3 in {output_folder}")
        
    return output_folder


def merge_video_audio(output_folder):
    video_file = os.path.join(output_folder, 'video.mp4')
    audio_file = os.path.join(output_folder, 'audio.mp3')
    merged_file = os.path.join(output_folder, 'merged_video.mp4')
    
    command = [
        'ffmpeg',
        '-i', video_file,
        '-i', audio_file,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        merged_file
    ]
    
    subprocess.run(command)
    print(f"Merged video saved to {merged_file}")
    
    return output_folder