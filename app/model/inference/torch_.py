import torch

from app.model.inference.infernece import Model


class TorchModel(Model):

    def __init__(self, config):
        super().__init__(config)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = config["model"].to(self.device)


    def __call__(self, dict):
        return self.model(**dict)