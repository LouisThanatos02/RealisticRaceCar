import os
import time
import threading
if __name__ == "__main__":
    os.system("gnome-terminal -e 'sudo python3 FullScr_cam.py'")
    os.system("gnome-terminal -e 'sudo python3 CarJoy_MotorOnly.py'")
    os.system("gnome-terminal -e 'sudo python3 CarJoy_ServoOnly.py'")
