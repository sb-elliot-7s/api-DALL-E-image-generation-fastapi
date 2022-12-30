from abc import ABC, abstractmethod
from fastapi import UploadFile
from image.schemas import CreateImageSchema, BaseImageSchema
from image_io.interfaces.image_io_service_interfaces import ImageIOServiceInterface


class ImageAIServiceInterface(ABC):

    @abstractmethod
    async def create_images(self, data: CreateImageSchema, image_io_service: ImageIOServiceInterface): pass

    @abstractmethod
    async def update_image(self, image: UploadFile, mask: UploadFile, data: CreateImageSchema,
                           image_io_service: ImageIOServiceInterface): pass

    @abstractmethod
    async def create_variation_image(
            self, image: UploadFile, data: BaseImageSchema, image_io_service: ImageIOServiceInterface): pass

    @staticmethod
    @abstractmethod
    async def delete_image(filename: str, image_io_service: ImageIOServiceInterface): pass
