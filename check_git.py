import subprocess
import sys

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

status = run("git status -s")
print(f"Git status length: {len(status)}")
with open("/tmp/real_git_status.txt", "w") as f:
    f.write(status)
