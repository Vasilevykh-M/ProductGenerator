import onnxruntime as ort
import os

from app.model.inference.infernece import Model


class OrtModel(Model):
    def __init__(self, config):
        super().__init__(config)

        if not os.path.exists(config["model"]):
            print("Файл не найден")

        self.ort_sess = ort.InferenceSession(config["model"])
        self.output = config["output"]

    def __call__(self, dict):
        super.__call__()
        return self.ort_sess.run(self.output, dict)