"""
This module is the main module in this package. It loads emotion recognition model from a file,
shows a webcam image, recognizes face and it's emotion and draw emotion on the image.
"""
from cv2 import WINDOW_NORMAL

import cv2
from face_detect import find_faces
from image_commons import nparray_as_image, draw_with_alpha
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime


def _load_emoticons(emotions):
    """
    Loads emotions images from graphics folder.
    :param emotions: Array of emotions names.
    :return: Array of emotions graphics.
    """
    return [nparray_as_image(cv2.imread('graphics/%s.png' % emotion, -1), mode=None) for emotion in emotions]

def printInfo(val):
    print val

def show_piCam(model, emoticons,window_size=None,window_name='PiCam', update_time=10):
    printInfo('showing pi cam')

    campaign = []
    faces = []
    emotion = {}
    
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate=32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    #allow the camera to warm up
    time.sleep(0.1)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        # print('in frame for loop')
        image = frame.array
        # printInfo('frame captured')
        count = 0
        for normalized_face, (x, y, w, h) in find_faces(image):
            emotion={}
            #printInfo("face found")
            count +=1
            prediction = model.predict(normalized_face)  # do prediction
            if cv2.__version__ != '3.1.0':
                print(prediction)
                prediction = prediction[0]

            #print "Found {0} face is {1}".format(count,emotions[prediction])
            emotion["face"] = count
            emotion["emotion"]=emotions[prediction]
            emotion["timestamp"]=str(datetime.datetime.now())
            #print emotions[prediction]
            #image_to_draw = emoticons[prediction]
            #image.setflags(write=1)
            #draw_with_alpha(image, image_to_draw, (x, y, w, h))
            faces.append(emotion)
            
        campaign.append(faces)
        cv2.imshow("Frame", image)
        # read_value, webcam_image = vc.read()
        image = frame.array
        # key = cv2.waitKey(update_time)
        # show the frame
        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            print faces
            break




def show_webcam_and_run(model, emoticons, window_size=None, window_name='webcam', update_time=10):
    """
    Shows webcam image, detects faces and its emotions in real time and draw emoticons over those faces.
    :param model: Learnt emotion detection model.
    :param emoticons: List of emotions images.
    :param window_size: Size of webcam image window.
    :param window_name: Name of webcam image window.
    :param update_time: Image update time interval.
    """
    cv2.namedWindow(window_name, WINDOW_NORMAL)
    if window_size:
        width, height = window_size
        cv2.resizeWindow(window_name, width, height)

    vc = cv2.VideoCapture(0)
    if vc.isOpened():
        read_value, webcam_image = vc.read()
    else:
        print("webcam not found")
        return

    while read_value:
        for normalized_face, (x, y, w, h) in find_faces(webcam_image):
            prediction = model.predict(normalized_face)  # do prediction
            if cv2.__version__ != '3.1.0':
                prediction = prediction[0]

            image_to_draw = emoticons[prediction]
            draw_with_alpha(webcam_image, image_to_draw, (x, y, w, h))

        cv2.imshow(window_name, webcam_image)
        read_value, webcam_image = vc.read()
        key = cv2.waitKey(update_time)

        if key == 27:  # exit on ESC
            break

    cv2.destroyWindow(window_name)


if __name__ == '__main__':
    emotions = ['neutral', 'anger', 'disgust', 'happy', 'sadness', 'surprise']
    emoticons = _load_emoticons(emotions)

    # load model
    if cv2.__version__ == '3.1.0':
        fisher_face = cv2.face.createFisherFaceRecognizer()
    else:
        fisher_face = cv2.createFisherFaceRecognizer()
    fisher_face.load('models/emotion_detection_model.xml')

    # use learnt model
    window_name = 'PiCam (press q to exit)'
    # window_name = 'WEBCAM (press ESC to exit)'
    # show_webcam_and_run(fisher_face, emoticons, window_size=(1600, 1200), window_name=window_name, update_time=8)
    show_piCam(fisher_face, emoticons, window_size=(1600, 1200), window_name=window_name, update_time=8)
