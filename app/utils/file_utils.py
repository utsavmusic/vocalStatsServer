import zipfile
import tempfile
from pathlib import Path
from typing import List
from fastapi.responses import FileResponse

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
        # Create a temporary directory to store the zip file
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / f"{archive_name}.zip"
            
            # Create zip file containing all specified files
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in files:
                    # Get the relative path within the output directory
                    relative_path = file.relative_to(output_dir)
                    zipf.write(file, arcname=relative_path)

            # Return the zip file as a response
            return FileResponse(
                zip_path,
                filename=f"{archive_name}.zip",
                media_type='application/zip'
            )
    
    except Exception as e:
        raise Exception(f"Error creating zip archive: {str(e)}")
