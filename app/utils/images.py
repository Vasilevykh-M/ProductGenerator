import numpy as np
import torch
from PIL import Image


def resizeWithPadding(image: Image, size: tuple[int, int])-> Image:
    width, height = image.size

    resizeCoefW = 0
    resizeCoefH = 0

    needH =  size[0]
    needW = size[1]

    if height / width > needH / needW:
        resizeCoefW = int(height * needW / needH - width)

    if height / width < needH / needW:
        resizeCoefH = int(needH * width / needW - height)

    result = Image.new(image.mode, (width + resizeCoefW, height + resizeCoefH), (255, 255, 255))

    result.paste(image, (resizeCoefW, resizeCoefH))

    return result.resize(size)


class normalize:
    def __init__(self, mean=None, std=None, div=255):
        self.mean = mean if mean is not None else 0.0
        self.std = std if std is not None else 1.0
        self.div = div

    def __call__(self, img):
        img /= self.div
        img -= self.mean
        img /= self.std

        return img


class tonumpy:
    def __init__(self):
        pass

    def __call__(self, img):
        img = np.array(img, dtype=np.float32)
        return img


class totensor:
    def __init__(self):
        pass

    def __call__(self, img):
        img = img.transpose((2, 0, 1))
        img = torch.from_numpy(img).float()

        return img