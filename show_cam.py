import cv2
import numpy as np
from thread_cam import CSI_Camera

show_fps = True

# Simple draw label on an image; in our case, the video frame
def draw_label(cv_image, label_text, label_position):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (255,255,255)
    # You can get the size of the string with cv2.getTextSize here
    cv2.putText(cv_image, label_text, label_position, font_face, scale, color, 1, cv2.LINE_AA)

# Read a frame from the camera, and draw the FPS on the image if desired
# Return an image
def read_camera(csi_camera,display_fps):
    _ , camera_image=csi_camera.read()
    if display_fps:
        draw_label(camera_image, "Frames Displayed (PS): "+str(csi_camera.last_frames_displayed),(10,20))
        draw_label(camera_image, "Frames Read (PS): "+str(csi_camera.last_frames_read),(10,40))
    return camera_image

# Good for 1280x720
# DISPLAY_WIDTH=640
# DISPLAY_HEIGHT=360
# For 1920x1080
DISPLAY_WIDTH=1920
DISPLAY_HEIGHT=1080

# 1920x1080, 30 fps
SENSOR_MODE_1080=2
# 1280x720, 60 fps
SENSOR_MODE_720=3

def start_cameras():
    camera = CSI_Camera()
    camera.create_gstreamer_pipeline(
            sensor_id=0,
            sensor_mode=SENSOR_MODE_720,
            framerate=30,
            flip_method=0,
            display_height=DISPLAY_HEIGHT,
            display_width=DISPLAY_WIDTH,
    )
    camera.open(camera.gstreamer_pipeline)
    camera.start()

    cv2.namedWindow("CSI Cameras", cv2.WINDOW_AUTOSIZE)

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
        while(True):
            image=read_camera(camera,show_fps)
            # We place both images side by side to show in the window
            camera_images = image
            cv2.imshow("CSI Cameras", camera_images)
            camera.frames_displayed += 1
            # This also acts as a frame limiter
            # Stop the program on the ESC key
            if (cv2.waitKey(20) & 0xFF) == 27:
                break   

    finally:
        camera.stop()
        camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_cameras()
