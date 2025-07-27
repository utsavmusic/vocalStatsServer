import os
import subprocess
from pathlib import Path
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
        
        # Create output directory in the project's tmp folder
        output_dir = os.path.abspath("tmp/output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Clean up any existing files in the output directory
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

        print(f"Output will be saved to: {output_dir}")
        
        command = get_spleeter_command(
            docker_image=self.docker_image,
            input_dir=input_dir,
            output_dir=output_dir,
            file_name=input_file_name,
            stems=stems
        )
        
        print("Running command:", " ".join(command))
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Print command output for debugging
        print("Command output:")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            raise Exception(f"Spleeter failed with error: {result.stderr}")
            
        # Verify files were created
        output_files = list(Path(output_dir).rglob("*.*"))
        print(f"Found {len(output_files)} files in output directory:")
        for f in output_files:
            print(f" - {f}")
            
        if not output_files:
            raise Exception("No output files were created by Spleeter")
            
        return output_dir
