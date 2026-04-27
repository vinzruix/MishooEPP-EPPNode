import cv2


class Multimedia:

    @staticmethod
    def take_photo_camera():
        capture = cv2.VideoCapture(0)
        frame = None

        for _ in range(10):
            ret, frame = capture.read()

        capture.release()

        return frame

    @staticmethod
    def cut_image(image,bounds):
        x1, y1, x2, y2 = map(int, bounds)
        return image[y1:y2,x1:x2]
