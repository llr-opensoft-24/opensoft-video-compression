# Video Processing and Uploading into GridFS

1. Clone and create, activate virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

2. Install the required libraries
```
pip3 install -r requirements.txt
```

3. Add the required credentials and other variables to `.env` file following the `.env.example` template
```
touch .env
```

4. Run the python script as standalone process
```
python3 compress_and_upload.py <file_name>
```

This will compress the given video into multiple resolutions and upload it into the MongoDB GridFS Location mentioned.
