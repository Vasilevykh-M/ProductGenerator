from app.model.generation_model import InpaintingModel
from app.model.gpt_tune import DescriptionModel
from app.modules.NeuralNetworks.background_remover_model import BackGroundRemover_


class Generator:
    def __init__(self, preprocessor, inpainting, blip):
        self.preprocessor = BackGroundRemover_(preprocessor)
        self.inpainting = InpaintingModel(inpainting)
        self.blip = DescriptionModel(blip)

    def __call__(self, image, y_pos, scale, promt, name):
        image, mask = self.preprocessor(image, scale, y_pos)
        text = self.blip(name)
        result = self.inpainting(image, mask, promt)
        return image, text