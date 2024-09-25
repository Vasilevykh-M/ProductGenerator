from app.model.inference.infernece import Model


class TrtModel(Model):

    def __init__(self, config):
        super().__init__(config)


    def __call__(self, dict):
        super.__call__()