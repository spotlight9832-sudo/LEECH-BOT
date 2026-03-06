import subprocess
import os

try:
    subprocess.run(['git', 'add', 'web/wserver.py'])
    subprocess.run(['git', 'commit', '-m', 'Fix stream URL and download link structures\n\nFixing link structures to match Heroku routes precisely and switching video source to https.'])
    print("Committed successfully")
except Exception as e:
    print(f"Error: {e}")
