from abc import ABC, abstractmethod


class ImageIOServiceInterface(ABC):
    @abstractmethod
    async def read_image(self, filename: str): pass

    @abstractmethod
    async def write_image(self, image: bytes, filename: str): pass

    @abstractmethod
    async def remove_image(self, filename: str): pass
