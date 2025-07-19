from abc import ABC, abstractmethod

class SeparationModel(ABC):
    @abstractmethod
    def separate(self, audio_file: str, stems: int) -> str:
        """
        Separate audio into stems and return the output directory.
        """
        pass
