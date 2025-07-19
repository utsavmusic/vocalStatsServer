import os
import subprocess
from .separation_model import SeparationModel
from app.foundation.docker_commands import get_spleeter_command
from app.foundation.constants import DOCKER_IMAGE_SPLEETER

class SpleeterModel(SeparationModel):
    def __init__(self, docker_image: str = DOCKER_IMAGE_SPLEETER):
        self.docker_image = docker_image

    def separate(self, audio_file: str, stems: int) -> str:
        # Get absolute paths
        input_dir = os.path.dirname(os.path.abspath(audio_file))
        input_file_name = os.path.basename(audio_file)
        output_dir = "/tmp/output"

        command = get_spleeter_command(
            docker_image=self.docker_image,
            input_dir=input_dir,
            output_dir=output_dir,
            file_name=input_file_name,
            stems=stems
        )

        subprocess.run(command, check=True)
        return output_dir
