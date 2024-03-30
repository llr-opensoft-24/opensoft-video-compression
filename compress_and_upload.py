# File to compress video files into different resolutions and save
import os, sys
from gridfs import GridFSBucket
from pymongo import MongoClient

VIDEOS_DB_URI = os.getenv("VIDEOS_DB_URI")

if __name__ == "__main__":
    input_filename = sys.argv[1]

    if not os.path.exists(input_filename):
        print(f"File {input_filename} does not exist")
        sys.exit(1)

    base_filename = os.path.basename(input_filename)

    RESOLUTIONS = {
        "4K": "3840:2160",
        "1080p": "1920:1080",
        "720p": "1280:720",
        "480p": "854:480",
        "360p": "640:360"
    }

    # Compress the video into different resolutions
    for resolution, size in RESOLUTIONS.items():
        output_filename = f"{base_filename.split('.')[0]}_{resolution}.{base_filename.split('.')[1]}"

        if os.path.exists(output_filename):
            print(f"File {output_filename} already exists")
            continue

        os.system(f"ffmpeg -i {input_filename} -vf \"scale={size}\" {output_filename}")

        print(f"Compressed {input_filename} into {output_filename} with resolution {resolution}")

    # Upload the compressed files to GridFS
    videos_client = MongoClient(VIDEOS_DB_URI)
    videos_db = videos_client['sample_mflix']

    grid_fs_bucket = GridFSBucket(videos_db, bucket_name="video_files")

    for resolution, _ in RESOLUTIONS.items():
        output_filename = f"{base_filename.split('.')[0]}_{resolution}.{base_filename.split('.')[1]}"

        with open(output_filename, 'rb') as file:
            file_id = grid_fs_bucket.upload_from_stream(output_filename, file)

            print(f"File uploaded as {file_id}")
