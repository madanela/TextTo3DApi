from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, BaseSettings
from tempfile import NamedTemporaryFile, TemporaryDirectory
import torch
import subprocess

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
# from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget
from shap_e.util.notebooks import decode_latent_mesh

class Settings(BaseSettings):
    blender_executable_path: str = "blender"  # Can be set via environment variable

settings = Settings()


if torch.cuda.is_available():
    DEFAULT_DEVICE = "cuda"
else:
    DEFAULT_DEVICE = "cpu"
    
device = torch.device(DEFAULT_DEVICE)


xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion'))

app = FastAPI()

@app.get("/generate_3d_mesh")
async def generate_3d_mesh(prompt: str,batch_size: int = 1,guidance_scale: float = 15.0):
    try:
        latents = sample_latents(
            batch_size=batch_size,
            model = model,
            diffusion=diffusion,
            guidance_scale=guidance_scale,
            model_kwargs=dict(texts=[prompt] * batch_size),
            progress=True,
            clip_denoised=True,
            use_fp16=True,
            use_karras=True,
            karras_steps = 64,
            sigma_min=1e-3,
            sigma_max=160,
            s_churn=0
        )
        with TemporaryDirectory() as temp_dir:
            mesh_paths = []
            for i, latent in enumerate(latents):
                with NamedTemporaryFile(dir=temp_dir, suffix=".obj", delete=False) as temp_file:
                    decode_latent_mesh(xm, latent).tri_mesh().write_obj(temp_file.name)
                    mesh_paths.append(temp_file.name)
            
            # Run Blender subprocess
            blender_file = f"{temp_dir}/texture.blend"
            python_script = f"{temp_dir}/blender_texture.py"
            command = [settings.blender_executable_path, "-b", blender_file, "-P", python_script]
            process = subprocess.Popen(command)
            retcode = process.wait()

            if retcode != 0:
                raise RuntimeError(f"Blender subprocess terminated with return code {retcode}")

            return FileResponse(mesh_paths[0], filename="example_mesh_0.usdz", media_type="application/octet-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))