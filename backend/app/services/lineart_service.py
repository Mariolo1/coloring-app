from __future__ import annotations

import cv2
import numpy as np
from PIL import Image


class LineArtService:
    def to_coloring_page(self, image: Image.Image) -> Image.Image:
        rgb = np.array(image.convert('RGB'))
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 55, 140)

        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)

        binary = cv2.bitwise_not(edges)
        binary = cv2.threshold(binary, 220, 255, cv2.THRESH_BINARY)[1]
        return Image.fromarray(binary)
