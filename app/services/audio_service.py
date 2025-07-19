from app.models.model_factory import ModelFactory

class AudioService:
    def __init__(self, model_name: str = "spleeter"):
        self.model = ModelFactory.get_model(model_name)

    def process_audio(self, file_path: str, stems: int):
        return self.model.separate(file_path, stems)
