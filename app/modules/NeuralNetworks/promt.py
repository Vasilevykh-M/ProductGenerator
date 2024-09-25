from app.model.clip_model import ClipModel


class ClipModule():
    def __init__(self, base, config):
        self.base = base

        labels = self.base.getRows(query=f"SELECT id, name_object FROM promt")
        self.model = ClipModel(config, labels)
    def __call__(self, img):
        idx = self.model(img)
        query = f"SELECT * FROM promt WHERE id = {idx}"
        return self.base.getRow(query)

