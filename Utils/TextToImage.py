from diffusers import StableDiffusionPipeline
import torch

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
# pipe = pipe.to("cuda")

prompt = "a cowboy hugging a cactus"
image = pipe(prompt).images[0]

image.save("astronaut_rides_horse.png")
