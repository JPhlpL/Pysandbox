import time
import os
from poc_compare_utils import (download_youtube_video_pytube, download_youtube_video_ytdlp, split_youtube_video_pytube, split_youtube_video_ytdlp, merge_video_audio)

def get_incremented_filename(base_name, extension):
    i = 1
    while True:
        filename = f"{base_name}_{i}.{extension}"
        if not os.path.exists(filename):
            return filename
        i += 1

def merger_func(video_url, base_folder, func_name, time_log_file):
    # Timer for the split function
    start_time = time.time()
    base_output_folder = func_name(video_url, base_folder)
    end_time = time.time()
    split_process_time = (end_time - start_time) * 1000  # convert to milliseconds
    
    # Log the process time for the split function
    with open(time_log_file, 'a') as f:
        f.write(f"{func_name.__name__} -> {split_process_time:.2f} ms\n")
    
    # Timer for the merge function
    start_time = time.time()
    merge_video_audio(base_output_folder)
    end_time = time.time()
    merge_process_time = (end_time - start_time) * 1000  # convert to milliseconds

    # Log the merge process time separately if needed (optional)
    with open(time_log_file, 'a') as f:
        f.write(f"merge_video_audio -> {merge_process_time:.2f} ms\n")
    
    return base_output_folder

def log_time(func, video_url, folder, time_log_file):
    start_time = time.time()
    result = func(video_url, folder)
    end_time = time.time()
    process_time = (end_time - start_time) * 1000  # convert to milliseconds
    # Log the process time for the download function
    with open(time_log_file, 'a') as f:
        f.write(f"{func.__name__} -> {process_time:.2f} ms\n")
    return result

if __name__ == "__main__":
    # List of video URLs
    video_urls = [
        "https://www.youtube.com/watch?v=q-_ezD9Swz4",
        "https://www.youtube.com/watch?v=WR1ydijTx5E",
        "https://www.youtube.com/watch?v=cvK0__7wmtM",
        "https://www.youtube.com/watch?v=ehTIhQpj9ys",
        "https://www.youtube.com/watch?v=rJKSxIdQVSA"
    ]
    
    # Get incremented filename for logging
    time_log_file = get_incremented_filename('process_times', 'txt')
    
    for video_url in video_urls:
        # Split ytdlp method
        if merger_func(video_url, 'ytdlp_split_sample', split_youtube_video_ytdlp, time_log_file):
            print(f'split ytdlp method done for {video_url}!')
        
        # Split pytube method
        if merger_func(video_url, 'pytube_split_sample', split_youtube_video_pytube, time_log_file):
            print(f'split pytube method done for {video_url}!')
        
        # One mp4 ytdlp method
        if log_time(download_youtube_video_ytdlp, video_url, 'ytdlp_one_sample', time_log_file):
            print(f'one mp4 ytdlp method done for {video_url}!')
        
        # One mp4 pytube method
        if log_time(download_youtube_video_pytube, video_url, 'pytube_one_sample', time_log_file):
            print(f'one mp4 pytube method done for {video_url}!')
