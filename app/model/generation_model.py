import torch
import random
from diffusers import DiffusionPipeline


class InpaintingModel:
    def __init__(self, engine):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_id = "yahoo-inc/photo-background-generation"
        self.pipeline = DiffusionPipeline.from_pretrained(
            self.model_id, custom_pipeline=self.model_id,
            cache_dir='/tmp/models')

        # self.pipeline = ORTStableDiffusionPipeline.from_pretrained(
        #     self.model_id,
        #     custom_pipeline=self.model_id,
        #     cache_dir='/tmp/models',
        #     export=True)

    def __call__(self, image, mask, prompt):
        seed = random.randint(1, 100)
        generator = torch.Generator(device=self.device).manual_seed(seed)
        cond_scale = 1.0
        return self.pipeline(
                prompt=prompt, image=image, mask_image=mask, control_image=mask,
                num_images_per_prompt=1, generator=generator, num_inference_steps=100,
                guess_mode=False, controlnet_conditioning_scale=cond_scale).images[0]