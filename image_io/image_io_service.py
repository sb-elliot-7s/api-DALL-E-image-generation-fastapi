from pathlib import Path
from fastapi import HTTPException, status
from image_io.interfaces.image_io_service_interfaces import ImageIOServiceInterface
import aiofiles


def image_not_found(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FileNotFoundError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')

    return wrapper


class ImageIOService(ImageIOServiceInterface):

    def __init__(self, path: str):
        self._path = path

    @image_not_found
    async def read_image(self, filename: str):
        path = f'{self._path}/{filename}'
        async with aiofiles.open(path, mode='rb') as f:
            image = await f.read()
        return image

    @image_not_found
    async def write_image(self, image: bytes, filename: str):
        path = f'{self._path}/{filename}'
        async with aiofiles.open(path, mode='wb') as f:
            await f.write(image)

    @image_not_found
    async def remove_image(self, filename: str):
        path = Path(f'{self._path}/{filename}')
        try:
            path.unlink()
        except OSError as e:
            raise OSError(e.args[-1])
