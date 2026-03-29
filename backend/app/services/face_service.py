from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image


@dataclass
class FaceCropResult:
    image: Image.Image
    bbox: tuple[int, int, int, int]


class FaceService:
    def __init__(self) -> None:
        self.detector = mp.solutions.face_detection.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.55,
        )

    def extract_face_region(self, image: Image.Image) -> Optional[FaceCropResult]:
        rgb = np.array(image.convert('RGB'))
        result = self.detector.process(rgb)
        if not result.detections:
            return None

        detection = result.detections[0]
        box = detection.location_data.relative_bounding_box
        h, w, _ = rgb.shape

        x = max(int(box.xmin * w), 0)
        y = max(int(box.ymin * h), 0)
        bw = max(int(box.width * w), 1)
        bh = max(int(box.height * h), 1)

        pad_x = int(bw * 0.45)
        pad_y = int(bh * 0.55)

        x1 = max(x - pad_x, 0)
        y1 = max(y - pad_y, 0)
        x2 = min(x + bw + pad_x, w)
        y2 = min(y + bh + pad_y, h)

        crop = rgb[y1:y2, x1:x2]
        if crop.size == 0:
            return None

        face_img = Image.fromarray(crop)
        return FaceCropResult(image=face_img, bbox=(x1, y1, x2, y2))
