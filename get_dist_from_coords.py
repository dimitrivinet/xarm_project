
import pyrealsense2 as rs
import numpy as np
import time

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while 1:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())

        interest_point = [480//2, 640//2]
        interest_range = 2
        interest_values = []
        for y in range(interest_point[0] - interest_range, interest_point[0] + interest_range):
            for x in range(interest_point[1] - interest_range, interest_point[1] + interest_range):
                interest_values.append(depth_image[x, y])

        depth = np.min(interest_values)

        print(depth)

finally:
    # Stop streaming
    pipeline.stop()
