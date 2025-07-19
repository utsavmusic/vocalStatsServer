# core/docker_command.py

def get_spleeter_command(docker_image: str, input_dir: str, output_dir: str, file_name: str, stems: int):
    """
    Build the docker command for running spleeter.
    """
    return [
        "docker", "run", "--rm",
        "-v", f"{input_dir}:/input",
        "-v", f"{output_dir}:/output",
        docker_image,
        "separate",
        "-p", f"spleeter:{stems}stems",
        "-o", "/output",
        f"/input/{file_name}"
    ]
