import rospy
from cv_bridge import CvBridge
import numpy as np

from invigorate_msgs.srv import *

class MAttNetClient():
    def __init__(self):
        self._br = CvBridge()
        self._client = rospy.ServiceProxy('mattnet_server', MAttNetGrounding)

    def ground(self, img, bboxes, expr, cls):
        req = MAttNetGroundingRequest()
        img_msg = self._br.cv2_to_imgmsg(img)
        req.img = img_msg
        req.cls = cls.flatten().tolist()
        req.bbox = bboxes.flatten().tolist()

        # HACK: We here standardize the expression using standard names
        # for visual grounding of MattNet, for fair comparison with the
        # original INVIGORATE published in RSS 2021.
        expr = expr.replace('remote controller', 'remote')
        expr = expr.replace('cell phone', 'phone')
        expr = expr.replace('sports ball', 'ball')
        req.expr = expr

        resp = self._client(req)
        grounding_scores = np.array(list(resp.ground_prob))

        return grounding_scores