import subprocess


# Kills all Python3 processes and then runs __init__.py.
# This was to avoid the oserror
def run():
    subprocess.Popen("sudo pkill -9 python3 && sudo python3 __init__.py 2>/dev/null", shell=True)
    print("running __init__")
    subprocess.Popen("sudo python3 motionRecord.py 2>/dev/null", shell=True)
    print("running motionRecord")

run()


