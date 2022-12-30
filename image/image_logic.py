import openai
from fastapi import UploadFile
from settings import get_settings
from .schemas import CreateImageSchema, BaseImageSchema
from .interfaces.image_ai_interfaces import ImageAIServiceInterface
from image_io.interfaces.image_io_service_interfaces import ImageIOServiceInterface
from .mixins import ImageUtilsMixin


class ImageLogic(ImageUtilsMixin, ImageAIServiceInterface):

    def __init__(self):
        openai.api_key = get_settings().open_ai_key

    async def create_images(self, data: CreateImageSchema, image_io_service: ImageIOServiceInterface):
        image_response: dict = openai.Image.create(**data.dict(exclude={'count'}), n=data.count)
        return await self.get_result(format_=data.response_format, image_io_service=image_io_service,
                                     image_response=image_response, text=data.prompt)

    async def update_image(self, image: UploadFile, mask: UploadFile, data: CreateImageSchema,
                           image_io_service: ImageIOServiceInterface):
        """ image: Must be a valid PNG file, less than 4MB, and square.
            mask: Must be a valid PNG file, less than 4MB, and have the same dimensions as image. """
        img_bytes = await image.read()
        mask_bytes = await mask.read()
        self.compare_images(image=img_bytes, mask=mask_bytes)
        image_response: dict = openai.Image.create_edit(
            image=img_bytes, mask=mask_bytes, **data.dict(exclude={'count'}), n=data.count)
        return await self.get_result(format_=data.response_format, image_response=image_response,
                                     image_io_service=image_io_service, text=data.prompt)

    async def create_variation_image(self, image: UploadFile, data: BaseImageSchema,
                                     image_io_service: ImageIOServiceInterface):
        """ image: Must be a valid PNG file, less than 4MB, and square. """
        img_bytes = await image.read()
        self.check_image(image=img_bytes)
        image_response: dict = openai.Image.create_variation(
            image=img_bytes, **data.dict(exclude={'count'}), n=data.count)
        return await self.get_result(format_=data.response_format, image_response=image_response,
                                     image_io_service=image_io_service, text=image.filename)

    @staticmethod
    async def delete_image(filename: str, image_io_service: ImageIOServiceInterface):
        await image_io_service.remove_image(filename=filename)
