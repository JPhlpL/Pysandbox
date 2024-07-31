import os
import yt_dlp
import re
import time

def sanitize_filename(filename):
    """
    Sanitizes the filename to remove any illegal characters.
    """
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def get_incremental_title_folder_name(base_output_folder, title):
    """
    Generates an incremental folder name based on the title within the base_output_folder.
    If the folder exists, appends a number to the folder name.
    """
    sanitized_title = sanitize_filename(title)
    title_folder_path = os.path.join(base_output_folder, sanitized_title)
    counter = 1
    while os.path.exists(title_folder_path):
        title_folder_path = os.path.join(base_output_folder, f"{sanitized_title}_{counter}")
        counter += 1
    return title_folder_path

def download_youtube_video_ytdlp(video_url, base_output_folder):
    start_time = time.time()
    
    # Ensure the output folder exists
    os.makedirs(base_output_folder, exist_ok=True)
    
    # Define options for best quality video automatically
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(base_output_folder, 'video.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegMetadata'
        }]
    }

    # Download best quality video with audio and extract video info
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=True)
    
    end_time = time.time()
    processing_time = end_time - start_time

    # Extract the necessary video information
    video_info = {
        'title': info_dict.get('title', 'Unknown'),
        'url': video_url,
        'resolution': f"{info_dict.get('width', 'Unknown')}x{info_dict.get('height', 'Unknown')}",
        'filesize_mb': round(info_dict.get('filesize', 0) / (1024 * 1024), 2) if info_dict.get('filesize') else 'Unknown',
        'audio_kbps': info_dict.get('abr', 'Unknown'),
        'ext': info_dict.get('ext', 'Unknown'),
        'processing_time_seconds': round(processing_time, 2)
    }

    # Create a directory named after the video title with incremental naming if needed
    title_folder_path = get_incremental_title_folder_name(base_output_folder, video_info['title'])
    os.makedirs(title_folder_path, exist_ok=True)

    # Move the downloaded video and info file to the title directory
    os.rename(os.path.join(base_output_folder, f"video.{video_info['ext']}"), os.path.join(title_folder_path, f"video.{video_info['ext']}"))
    info_file_path = os.path.join(title_folder_path, 'video_info.txt')
    with open(info_file_path, 'w') as info_file:
        for key, value in video_info.items():
            info_file.write(f"{key}: {value}\n")

    print(f"Video downloaded to {os.path.join(title_folder_path, 'video.' + video_info['ext'])}")
    print(f"Video information saved to {info_file_path}")
        
    return title_folder_path

# Example usage:
if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=SKh6ZFSY_Ek&t=494s"
    base_output_folder = "output/ytdlp_downloaded_vids/"
    download_folder = download_youtube_video_ytdlp(video_url, base_output_folder)
    print(f"Downloaded video to folder: {download_folder}")
