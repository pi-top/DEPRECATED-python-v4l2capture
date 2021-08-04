#!/usr/bin/python
#
# python-v4l2capture
#
# This file is an example on how to capture a picture with
# python-v4l2capture.
#
# 2009, 2010, 2015, 2016 Fredrik Portstrom <https://portstrom.com>
#
# I, the copyright holder of this file, hereby release it into the
# public domain. This applies worldwide. In case this is not legally
# possible: I grant anyone the right to use this work for any
# purpose, without any conditions, unless such conditions are
# required by law.

import argparse
import Image
import select
import time
import v4l2capture


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delay", default = 0, dest = "delay", help =
        "Number of seconds to wait between starting the camera and taking "
        "the picture. Some cameras take a few seconds to get bright enough. "
        "[default: %(default)s]", type = float)
    parser.add_argument("--image-size-x", default = 1280, dest = "image_size_x",
        help = "The width of the image to capture. [default: %(default)s]",
        type = int)
    parser.add_argument("--image-size-y", default = 1024, dest = "image_size_y",
        help = "The height of the image to capture. [default: %(default)s]",
        type = int)
    parser.add_argument("--quiet", action = "store_true", dest = "quiet")
    parser.add_argument("--output", default = "image.jpg", dest = "output_path",
        help = "Path of the image file to save. [default: %(default)s]")
    parser.add_argument("--video-device", default = "/dev/video0",
        dest = "video_device_path",
        help = "Path of the video device to open. [default: %(default)s]")
    options = parser.parse_args()

    # Open the video device.
    video = v4l2capture.Video_device(options.video_device_path)

    # Suggest an image size to the device. The device may choose and
    # return another size if it doesn't support the suggested one.
    size_x, size_y = video.set_format(
        options.image_size_x, options.image_size_y)

    # Create a buffer to hold image data. This must be done before calling
    # 'start' if v4l2capture is compiled with libv4l2. Otherwise raises IOError.
    video.create_buffers(1)

    if options.delay:
        # Start the device. This lights the LED if it's a camera that has one.
        video.start()

        # Wait a little. Some cameras take a few seconds to get bright enough.
        time.sleep(options.delay)

        # Send the buffer to the device.
        video.queue_all_buffers()
    else:
        # Send the buffer to the device. Some devices require this to be done
        # before calling 'start'.
        video.queue_all_buffers()

        # Start the device. This lights the LED if it's a camera that has one.
        video.start()

    # Wait for the device to fill the buffer.
    select.select((video,), (), ())

    # The rest is easy :-)
    image_data = video.read()
    video.close()
    image = Image.frombytes("RGB", (size_x, size_y), image_data)
    image.save(options.output_path)
    if not options.quiet:
        print("Saved file '%s' (Size: %s x %s)" % (
            options.output_path, size_x, size_y))


if __name__ == "__main__":
    main()
