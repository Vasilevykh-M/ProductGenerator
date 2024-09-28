import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class DescriptionModel():

    def __init__(self, engine):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained("HamidRezaAttar/gpt2-product-description-generator")
        model = AutoModelForCausalLM.from_pretrained("HamidRezaAttar/gpt2-product-description-generator")
        self.pipeline = pipeline('text-generation', model, tokenizer=tokenizer, config={'max_length': 1600}, device=self.device)

        # self.pipeline = ORTStableDiffusionPipeline.from_pretrained(
        #     self.model_id,
        #     custom_pipeline=self.model_id,
        #     cache_dir='/tmp/models',
        #     export=True)

    def __call__(self, text):
        return self.pipeline(text)[0]['generated_text']
