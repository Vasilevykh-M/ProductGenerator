from PIL import ImageOps, Image
import numpy as np
from skimage.measure import label

from app.model.background_remover_model import BackGroundRemover

class BackGroundRemover_():

    def __init__(self, config, max_img_dim=(1280, 1280)):

        self.background_mask = BackGroundRemover(config, max_img_dim)
        self.max_img_dim = max_img_dim


    def keep_only_largest_cc(self, mask):
        # Convert to grayscale numpy array
        arr = np.asarray(mask.convert('L'))

        # Get largest connected component mask
        labels = label(arr < 255)
        if labels.max() == 0:
            return mask
        largestCC = labels == np.argmax(np.bincount(labels.flat)[1:]) + 1

        # Remove everything except largest CC
        mask = np.where(largestCC, arr, 255)
        return Image.fromarray(mask)

    def crop_empty_space(self, img, mask):
        # Convert to grayscale numpy array
        arr = np.asarray(mask.convert('L'))

        # Find X empty space boundaries
        x_mask = (~np.all(arr == 255, axis=0))
        x_from = x_mask.argmax()
        x_to = len(x_mask) - x_mask[::-1].argmax()

        # Find Y empty space boundaries
        y_mask = (~np.all(arr == 255, axis=1))
        y_from = y_mask.argmax()
        y_to = len(y_mask) - y_mask[::-1].argmax()

        # Crop empty space
        img_cropped = img.crop((x_from, y_from, x_to, y_to))
        mask_cropped = mask.crop((x_from, y_from, x_to, y_to))

        return img_cropped, mask_cropped

    def add_padding(self, img, mask, scale, y_pos):
        # Clip scale and position values
        scale = np.clip(scale, 0.1, 1.0)
        y_pos = np.clip(y_pos, 0.0, 1.0)

        # Compute paddings
        max_size = max(img.size[1], img.size[0])
        target_size = int(max_size / scale)
        pad_left = int((target_size - img.size[0]) * 0.5)
        pad_top = int((target_size - img.size[1]) * y_pos)
        pad_right = target_size - img.size[0] - pad_left
        pad_bottom = target_size - img.size[1] - pad_top

        # Pad image and mask
        padded_img = ImageOps.expand(img, border=(
            pad_left, pad_top, pad_right, pad_bottom))
        padded_mask = ImageOps.expand(mask, border=(
            pad_left, pad_top, pad_right, pad_bottom), fill='white')

        return padded_img, padded_mask

    def __call__(self, img, scale, y_pos, max_out_dim=(640, 640)):

        image = img.convert('RGB')

        img, mask = self.background_mask(image)

        mask = self.keep_only_largest_cc(mask)
        img, mask = self.crop_empty_space(img, mask)
        img, mask = self.add_padding(img, mask, scale, y_pos)
        img.thumbnail(max_out_dim)
        mask.thumbnail(max_out_dim)

        return img, mask