from app.model.generation_model import InpaintingModel
from app.model.gpt_tune import DescriptionModel
from app.modules.NeuralNetworks.background_remover_model import BackGroundRemover_


class Generator:
    def __init__(self, preprocessor, inpainting, decs_gen):
        self.preprocessor = BackGroundRemover_(preprocessor)
        self.inpainting = InpaintingModel(inpainting)
        self.decs_gen = DescriptionModel(decs_gen)

    def __call__(self, image, y_pos, scale, promt, name):
        image, mask = self.preprocessor(image, scale, y_pos)
        text = self.decs_gen(name)
        result = self.inpainting(image, mask, promt)
        return result, text