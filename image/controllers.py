from fastapi import APIRouter, status, UploadFile, Depends
from .service import ImageService
from .image_logic import ImageLogic
from .schemas import CreateImageSchema, BaseImageSchema, ImageResponseSchema
from image_io.image_io_service import ImageIOService
from settings import IMAGE_DIR

image_controllers = APIRouter(prefix='/images', tags=['images'])

api_data = {
    'generate': {'path': '/', 'status_code': status.HTTP_201_CREATED, 'response_model': ImageResponseSchema},
    'variation': {'path': '/variations', 'status_code': status.HTTP_201_CREATED, 'response_model': ImageResponseSchema},
    'update': {'path': '/', 'status_code': status.HTTP_200_OK, 'response_model': ImageResponseSchema},
    'delete': {'path': '/{filename}', 'status_code': status.HTTP_204_NO_CONTENT}
}


@image_controllers.post(**api_data.get('generate'))
async def generate_images(data: CreateImageSchema):
    return await ImageService(logic=ImageLogic()) \
        .create_images(data=data, image_io_service=ImageIOService(path=IMAGE_DIR))


@image_controllers.post(**api_data.get('variation'))
async def create_variation_image(image: UploadFile, data: BaseImageSchema = Depends(BaseImageSchema.as_form)):
    return await ImageService(logic=ImageLogic()) \
        .create_variation_image(data=data, image_io_service=ImageIOService(path=IMAGE_DIR), image=image)


@image_controllers.patch(**api_data.get('update'))
async def update_image(image: UploadFile, mask: UploadFile,
                       data: CreateImageSchema = Depends(CreateImageSchema.as_form)):
    return await ImageService(logic=ImageLogic()) \
        .update_image(data=data, image=image, mask=mask, image_io_service=ImageIOService(path=IMAGE_DIR))


@image_controllers.delete(**api_data.get('delete'))
async def delete_image(filename: str):
    await ImageService(logic=ImageLogic()) \
        .delete_image(filename=filename, image_io_service=ImageIOService(path=IMAGE_DIR))
