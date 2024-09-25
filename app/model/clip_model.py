import clip
import torch

from app.model.inference.ort_ import OrtModel
from app.model.inference.torch_ import TorchModel


class ClipModel:
    def __init__(self, config, data_label):

        self.engine = config['engine']

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if self.engine == "ort":
            _, self.preprocess = clip.load("ViT-B/32", device=self.device)
            self.model = OrtModel(config)
        if self.engine == "trt":
            pass
        if self.engine == "torch":
            model, self.preprocess = clip.load("ViT-B/32", device=self.device)
            self.model = TorchModel({"model": model})

        self.data_label = data_label
        self.text = clip.tokenize([i[1] for i in self.data_label]).to(self.device)

        if self.engine == 'ort':
            self.text = self.text.detach().to("cpu").numpy()

    def __call__(self, image):
        image = self.preprocess(image).unsqueeze(0).to(self.device)

        if self.engine == 'ort':
            image = image.detach().to("cpu").numpy()

        result = self.model({"image": image, "text": self.text})
        if not torch.is_tensor(result[0]):
            logits_per_image = torch.from_numpy(result[0])
        else:
            logits_per_image = result[0]
        idx = torch.argmax(logits_per_image.softmax(dim=-1)).item()
        return self.data_label[idx][0]
