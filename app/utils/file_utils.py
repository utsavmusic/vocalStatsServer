import zipfile
import shutil
import os
from pathlib import Path
from typing import List
from fastapi.responses import FileResponse
from datetime import datetime, timedelta

def create_zip_archive(files: List[Path], output_dir: Path, archive_name: str) -> FileResponse:
    """
    Create a zip archive containing the specified files and return it as a FastAPI FileResponse.

    Args:
        files: List of Path objects to include in the zip archive
        output_dir: Directory containing the files to be zipped
        archive_name: Base name for the zip archive (without extension)

    Returns:
        FastAPI FileResponse containing the zip archive
    """
    try:
        # Create a directory for zip files if it doesn't exist
        zip_dir = Path("temp/zips")
        zip_dir.mkdir(parents=True, exist_ok=True)

        # Create a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"{archive_name}_{timestamp}.zip"
        zip_path = zip_dir / zip_filename

        # Create zip file containing all specified files
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                if file.exists():
                    # Get the relative path within the output directory
                    try:
                        relative_path = file.relative_to(output_dir)
                        zipf.write(file, arcname=relative_path)
                    except ValueError:
                        # If file is not in output_dir, add it to the root of the zip
                        zipf.write(file, arcname=file.name)

        # Verify the zip file was created
        if not zip_path.exists():
            raise FileNotFoundError(f"Failed to create zip file at {zip_path}")

        # Return the zip file as a response
        return FileResponse(
            zip_path,
            filename=zip_filename,
            media_type='application/zip'
        )

    except Exception as e:
        raise Exception(f"Error creating zip archive: {str(e)}")

def cleanup_temp_and_tmp():
    """
    Deletes all files/folders inside temp/ and tmp/output (but not output folder itself),
    and all files/folders inside tmp except the output folder.
    """
    print("Cleaning up temp/ and tmp/output...")
    # Clean temp/
    temp_dir = Path('temp')
    if temp_dir.exists():
        for item in temp_dir.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Error deleting {item}: {e}")

    # Clean tmp/output/
    output_dir = Path('tmp/output')
    if output_dir.exists():
        for item in output_dir.iterdir():
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Error deleting {item}: {e}")

    # Clean tmp/, but skip output folder
    tmp_dir = Path('tmp')
    if tmp_dir.exists():
        for item in tmp_dir.iterdir():
            if item.name == 'output':
                continue
            try:
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Error deleting {item}: {e}")
