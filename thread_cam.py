# MIT License
# Copyright (c) 2019,2020 JetsonHacks
# See license
# A very simple code snippet
# Using two  CSI cameras (such as the Raspberry Pi Version 2) connected to a
# NVIDIA Jetson Nano Developer Kit (Rev B01) using OpenCV
# Drivers for the camera and OpenCV are included in the base image in JetPack 4.3+

# This script will open a window and place the camera stream from each camera in a window
# arranged horizontally.
# The camera streams are each read in their own thread, as when done sequentially there
# is a noticeable lag

import cv2
import numpy as np
import threading
from csi_camera import CSI_Camera

show_fps = True

# Simple draw label on an image; in our case, the video frame
def draw_label(cv_image, label_text, label_position):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (0,255,0)
    # You can get the size of the string with cv2.getTextSize here
    cv2.putText(cv_image, label_text, label_position, font_face, scale, color, 1, cv2.LINE_AA)

# Read a frame from the camera, and draw the FPS on the image if desired
# Return an image
def read_camera(csi_camera,display_fps):
    _ , camera_image=csi_camera.read()
    thread_name=[]
    thread_name=threading.enumerate()
    if display_fps:
        draw_label(camera_image, "FDPS: "+str(csi_camera.last_frames_displayed),(10,20))
        draw_label(camera_image, "FRPS: "+str(csi_camera.last_frames_read),(10,40))
        draw_label(camera_image,"Thread: "+str(threading.active_count()),(10,60))
        for i in range(threading.active_count()):
            draw_label(camera_image,"Thread%d_name: "%(i+1)+str(thread_name[i]),(10,60+((i+1)*20)))
    return camera_image

# Good for 1280x720
# DISPLAY_WIDTH=640
# DISPLAY_HEIGHT=360
# For 1920x1080
CAPTURE_WIDTH=1660
CAPTURE_HIEGHT=1100
DISPLAY_WIDTH=1920
DISPLAY_HEIGHT=1080
FARMERATE=25


# 1920x1080, 30 fps
SENSOR_MODE_1080=2
# 1280x720, 60 fps
SENSOR_MODE_720=3

def start_cameras():
    camera = CSI_Camera()
    camera.create_gstreamer_pipeline(
            capture_width=CAPTURE_WIDTH,
            capture_height=CAPTURE_HIEGHT,
            framerate=FARMERATE,
            flip_method=0,
            display_height=DISPLAY_HEIGHT,
            display_width=DISPLAY_WIDTH,
    )
    camera.open(camera.gstreamer_pipeline)
    camera.start()

    cv2.namedWindow("CSI Cameras", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("CSI Cameras",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    if (
        not camera.video_capture.isOpened()
    ):
        # Cameras did not open, or no camera attached

        print("Unable to open any cameras")
        # TODO: Proper Cleanup
        SystemExit(0)
    try:
        # Start counting the number of frames read and displayed
        camera.start_counting_fps()
        #right_camera.start_counting_fps()
        while cv2.getWindowProperty("CSI Cameras", 0) >= 0 :
            image=read_camera(camera,show_fps)
            # We place both images side by side to show in the window
            cv2.imshow("CSI Cameras", image)
            camera.frames_displayed += 1
            # This also acts as a frame limiter
            # Stop the program on the ESC key
            if (cv2.waitKey(50) & 0xFF) == 27:
                break   

    finally:
        camera.stop()
        camera.release()
        #right_camera.stop()
        #right_camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_cameras()
