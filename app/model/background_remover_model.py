from PIL import ImageOps, Image

import torch.nn.functional as F
import torchvision.transforms as transforms
import albumentations.pytorch as AP

import albumentations as A

import onnxruntime as ort

from app.utils.images import *

class BackGroundRemover():

    def __init__(self, config, max_img_dim=(1280, 1280)):

        if config['engine'] == "ort":
            self.remover = ort.InferenceSession(config['model'])

        self.transform = transforms.Compose(
            [
                tonumpy(),
                normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
                totensor(),
            ]
        )

        self.max_img_dim = max_img_dim

    def preproc(self, image):
        img = resizeWithPadding(image, self.max_img_dim)

        shape = img.size[::-1]
        x = self.transform(img)

        x = x.unsqueeze(0)
        return x, img, shape

    def postprocess(self, pred, shape):
        pred = torch.from_numpy(pred[0])

        pred = F.interpolate(pred, shape, mode="bilinear", align_corners=True).data.cpu()
        pred = pred.numpy().squeeze()

        mask = (np.stack([pred] * 3, axis=-1) * 255).astype(np.uint8)

        mask = Image.fromarray(mask.astype(np.uint8))

        mask = ImageOps.invert(mask)

        return mask

    def __call__(self, image):
        x, img, shape = self.preproc(image)

        pred = self.remover.run(
            ["mask"],
            {
                'pixel_values': x.cpu().detach().numpy()
            }
        )

        mask = self.postprocess(pred, shape)

        return img, mask