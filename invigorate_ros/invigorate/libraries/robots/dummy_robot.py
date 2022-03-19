import rospy
import cv2
import os.path as osp
import logging
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from config.config import *
from libraries.utils.log import LOGGER_NAME

USE_LIVE_CAMERA = False
USE_DATASET = False
DATASET_STRING = osp.join(ROOT_DIR, 'dataset/rss/{:s}/res/{:s}.png')

YCROP = (100, 440) # 540
XCROP = (300, 660) # 960

logger = logging.getLogger(LOGGER_NAME)

class DummyRobot():
    def __init__(self,
                 camera_topic=None):
        self._br = CvBridge()
        self.camera_topic = camera_topic

    def read_imgs(self):
        if USE_LIVE_CAMERA:
            assert isinstance(self.camera_topic, str)
            img_msg = rospy.wait_for_message(self.camera_topic, Image, timeout=10)
            img = self._br.imgmsg_to_cv2(img_msg, desired_encoding='bgr8')
            logger.info('img_size : {}'.format(img.shape))
            img = img[YCROP[0]:YCROP[1], XCROP[0]:XCROP[1]]
            logger.info('img_size : {}'.format(img.shape))
            depth = None

        elif USE_DATASET:
            img_name = raw_input('Enter data index: ')
            img_name = img_name.split(' ')
            img = cv2.imread(DATASET_STRING.format(img_name[0], img_name[1]))
            depth = None

        else:
            img_name = raw_input('Enter img name: ')
            img = cv2.imread(osp.join(ROOT_DIR, 'demo/' + img_name))
            # longest_side = max(img.shape)
            # scaler = 800. / longest_side
            # img = cv2.resize(img, None, fx=scaler, fy=scaler)
            depth = None

        return img, depth

    def grasp(self, grasp, is_target = False):
        print('Dummy execution of grasp {}'.format(grasp))
        return True

    def say(self, text):
        print('Dummy execution of say: {}'.format(text))
        return True

    def listen(self, timeout=None):
        print('Dummy execution of listen')
        text = raw_input("Enter: ")
        return text

    def move_arm_to_home(self):
        print('Dummy execution of move_arm_to_home')
        return