# main.py
import sys
sys.path.append('/workspace/dev_ws/src/background_removal')
import cv2 

# main.py
from utils import FPSmetric
from selfieSegmentation import MPSegmentation
from engine import Engine

if __name__ == '__main__':

    img = cv2.imread('/workspace/dev_ws/media/images/2024/IMG_6627.png')

    fpsMetric = FPSmetric()
    segmentationModule = MPSegmentation(threshold=0.8, bg_images_path='', bg_blur_ratio=(65, 65))
    selfieSegmentation = Engine(show=True, custom_objects=[segmentationModule, fpsMetric])
    img_result = selfieSegmentation.custom_processing(frame=img)

    h, w, _ = img_result.shape
    fc = 0.3

    img_result = cv2.resize(img_result, (int(fc*w), int(fc*h)))

    cv2.imshow("Test", img_result)
    cv2.waitKey(0)

    # -----------------------------
    # fpsMetric = FPSmetric()
    # segmentationModule = MPSegmentation(threshold=0.8, bg_images_path='', bg_blur_ratio=(65, 65))
    # selfieSegmentation = Engine(image_path='/workspace/WhatsApp Image 2023-12-25 at 8.25.16 AM.jpeg', show=True, custom_objects=[segmentationModule, fpsMetric])
    # selfieSegmentation.run()