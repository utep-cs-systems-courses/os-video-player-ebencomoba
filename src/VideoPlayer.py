#!/usr/bin/env python3

import threading
import cv2
import base64
from PCQueue import PCQueue


def extract_frames(fileName, framesQueue, maxFramesToLoad=999):
    # Open video file and read first image
    vidcap = cv2.VideoCapture(fileName)
    success, image = vidcap.read()

    print('Frame extraction started')
    count = 0
    while success and count < maxFramesToLoad:
        # Get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        # Encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        # Add the frame to the queue
        framesQueue.enqueue(image)
        print(f'Reading frame {count} {success}')

        # Go to next image
        success, image = vidcap.read()
        count += 1

    print('Frame extraction completed')
    framesQueue.kill()


def convert_to_grayscale(framesQueue, grayScaleQueue):
    print('Conversion to grayscale started')
    count = 0

    while framesQueue.isActive() or not framesQueue.isEmpty():
        # Get frame from first queue
        inputFrame = framesQueue.deque()
        print(f'Converting frame {count}')

        # Convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)

        # Save grayscale frame into second queue
        grayScaleQueue.enqueue(grayscaleFrame)

        count += 1

    print('Conversion to grayscale completed')
    grayScaleQueue.kill()


def display_frames(grayScaleQueue):
    count = 0

    # Go through each frame in the buffer until the queue is empty
    print('Started displaying all frames')
    while grayScaleQueue.isActive() or not grayScaleQueue.isEmpty():
        # Get the next frame
        frame = grayScaleQueue.deque()
        print(f'Displaying frame {count}')

        # Display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1

    print('Finished displaying all frames')
    # Cleanup the windows
    cv2.destroyAllWindows()


def main():
    filename = '../clip.mp4'
    framesQueue = PCQueue()
    grayScaleQueue = PCQueue()
    extraction_t = threading.Thread(target=extract_frames, args=(filename, framesQueue, 72,))
    extraction_t.start()
    conversion_t = threading.Thread(target=convert_to_grayscale, args=(framesQueue, grayScaleQueue,))
    conversion_t.start()
    display_t = threading.Thread(target=display_frames, args=(grayScaleQueue,))
    display_t.start()
    display_t.join()


if __name__ == "__main__":
    main()
