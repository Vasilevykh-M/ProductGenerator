from PIL import Image
from fastapi import File, UploadFile, APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from io import BytesIO
import base64

from starlette.responses import JSONResponse


def image2base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


class GenerateApi:
    def __init__(self, generator, clip):
        self.generator = generator
        self.clip = clip
        self.router = APIRouter()
        self.router.add_api_route(
            "/generate_background", self.generate_background, methods=["POST"])

        self.router.add_api_route(
            "/get_background_result", self.get_background_result, methods=["POST"])
        self.router.add_api_route(
            "/", lambda : JSONResponse(jsonable_encoder({"Hello world"}))
        )

    async def generate_background(self, img_file: UploadFile = File(...), y_pos: float = 0.0, scale: float = 0.0, prompt: str = "", name: str = ""):
        if all(ext not in img_file.filename for ext in ['.jpg', '.jpeg', '.png']):
            return HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f'File {img_file.filename} has unsupported extension type',
            )
        request_object_content = await img_file.read()
        img = Image.open(BytesIO(request_object_content))
        result_img, text = self.generator(img, y_pos, scale, prompt, name)
        json_data = jsonable_encoder({"img": image2base64(result_img), "description": text})
        return JSONResponse(json_data)

    async def get_background_result(self, img_file: UploadFile = File(...)):
        if all(ext not in img_file.filename for ext in ['.jpg', '.jpeg', '.png']):
            return HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f'File {img_file.filename} has unsupported extension type',
            )

        request_object_content = await img_file.read()
        img = Image.open(BytesIO(request_object_content))
        row = self.clip(img)

        json_data = jsonable_encoder({"y_pos": row[3], "scale": row[2], "prompt": row[1], "name": row[4]})
        return JSONResponse(json_data)

