from fastapi import UploadFile
from .interfaces.image_ai_interfaces import ImageAIServiceInterface
from .schemas import CreateImageSchema, BaseImageSchema
from image_io.interfaces.image_io_service_interfaces import ImageIOServiceInterface


class ImageService:
    def __init__(self, logic: ImageAIServiceInterface):
        self._logic = logic

    async def create_images(self, data: CreateImageSchema, image_io_service: ImageIOServiceInterface):
        return await self._logic.create_images(data=data, image_io_service=image_io_service)

    async def update_image(self, data: CreateImageSchema, image: UploadFile, mask: UploadFile,
                           image_io_service: ImageIOServiceInterface):
        return await self._logic.update_image(data=data, image=image, mask=mask, image_io_service=image_io_service)

    async def create_variation_image(
            self, image: UploadFile, data: BaseImageSchema, image_io_service: ImageIOServiceInterface
    ):
        return await self._logic.create_variation_image(data=data, image_io_service=image_io_service, image=image)

    async def delete_image(self, filename: str, image_io_service: ImageIOServiceInterface):
        await self._logic.delete_image(filename=filename, image_io_service=image_io_service)
