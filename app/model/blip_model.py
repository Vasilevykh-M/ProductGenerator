from transformers import AutoProcessor, BlipForConditionalGeneration

class BlipModel:
    def __init__(self, data_label):
        # self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = "cpu"
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        self.processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")

    def __call__(self, image):
        inputs = self.processor(images=image, return_tensors="pt").to(self.device)
        pixel_values = inputs.pixel_values

        generated_ids = self.model.generate(pixel_values=pixel_values, max_length=50)
        generated_caption = self.processor.batch_decode(generated_ids, skip_special_tokens=True)
        return generated_caption