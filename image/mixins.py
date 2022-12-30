from base64 import b64decode
from enum import Enum
from uuid import uuid4
from fastapi import HTTPException, status
from .schemas import ResponseFormat, ImageResponseSchema
from image_io.interfaces.image_io_service_interfaces import ImageIOServiceInterface
from PIL import Image
from io import BytesIO


class ImageExceptionEnum(str, Enum):
    MUST_BE_LESS_THAN_4_MB = 'must be less than 4 mb'
    MUST_BE_PNG_FORMAT = 'must be png format'
    MUST_BE_A_SQUARE = 'must be a square'
    MUST_BE_THE_SAME_SIZE = 'must be the same size'

    def get_exception(self, status_code: int = status.HTTP_400_BAD_REQUEST):
        return {
            ImageExceptionEnum.MUST_BE_LESS_THAN_4_MB: HTTPException(status_code, detail=f'Image {self.value}'),
            ImageExceptionEnum.MUST_BE_A_SQUARE: HTTPException(status_code, detail=f'Image {self.value}'),
            ImageExceptionEnum.MUST_BE_PNG_FORMAT: HTTPException(status_code, detail=f'Image {self.value}'),
            ImageExceptionEnum.MUST_BE_THE_SAME_SIZE: HTTPException(status_code, detail=f'Images {self.value}')
        }[self]


class ImageUtilsMixin:

    @staticmethod
    async def __save_images(response_data: dict, image_io_service: ImageIOServiceInterface):
        prompt = response_data.get('text')
        for image in response_data.get('images'):
            filename = f'{str(uuid4())[:10]}-{prompt}.png'
            img: bytes = b64decode(image['b64_json'])
            await image_io_service.write_image(filename=filename, image=img)

    async def get_result(self, format_: ResponseFormat, image_response: dict, image_io_service: ImageIOServiceInterface,
                         text: str):
        if format_ == ResponseFormat.URL:
            return image_response
        await self.__save_images({'text': text, 'images': image_response.get('data')}, image_io_service)
        return ImageResponseSchema(data={'detail': 'Images downloaded'})

    @staticmethod
    def check_image(image: bytes):
        if len(image) > 4194304:
            raise ImageExceptionEnum.MUST_BE_LESS_THAN_4_MB.get_exception()
        with Image.open(BytesIO(image)) as im:
            if im.format != 'PNG':
                raise ImageExceptionEnum.MUST_BE_PNG_FORMAT.get_exception()
            if im.width != im.height:
                raise ImageExceptionEnum.MUST_BE_A_SQUARE.get_exception()
            return im.width, im.height

    def compare_images(self, image: bytes, mask: bytes):
        img_size = self.check_image(image=image)
        mask_size = self.check_image(image=mask)
        if img_size != mask_size:
            raise ImageExceptionEnum.MUST_BE_THE_SAME_SIZE.get_exception()
