from app.models.spleeter_model import SpleeterModel

class ModelFactory:
    @staticmethod
    def get_model(model_name: str):
        if model_name.lower() == "spleeter":
            return SpleeterModel()
        else:
            raise ValueError(f"Unknown model: {model_name}")
