import os
import time
if __name__ == "__main__":
    os.system("gnome-terminal -e 'sudo python3 FullScr_cam.py'")
    time.sleep(1)
    os.system("gnome-terminal -e 'sudo python3 CarJoy_ServoOnly.py'")
