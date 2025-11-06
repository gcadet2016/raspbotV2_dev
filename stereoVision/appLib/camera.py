import appLib.env_detect as e
if e.is_raspberry_pi():
    from picamera2 import Picamera2
    from libcamera import Transform

class picam2:
    def __init__(self, id: int,
                size: tuple = (640, 480), 
                format: str = "RGB888", 
                buffer_count: int = 2):
        # self.size = size
        # self.format = format
        # self.buffer_count = buffer_count

        # size: tuple = (CAM_WIDTH, CAM_HEIGHT)
        # format: str = IMG_FMT  # good CPU format; convert to gray in cv2
        # buffer_count: int = 2    # keep latency low

        self.cam = Picamera2(index)
        camera_cfg = self.cam.create_preview_configuration(
            main={"size": size, "format": format},
            buffer_count=buffer_count,
            #transform=Transform(vflip=1, hflip=1)
        )
        self.cam.configure(camera_cfg)
        # Optional: hint FPS/Exposure. Commented to keep defaults.
        # cam.set_controls({"FrameDurationLimits": (33333, 33333)})  # ~30 fps
        self.cam.start()
