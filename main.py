
from fastapi import FastAPI, File, UploadFile
import easyocr
from PIL import Image
import numpy as np
import io
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
reader = easyocr.Reader(['en', 'es'], gpu=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    np_image = np.array(image)

    result = reader.readtext(np_image, detail=0)
    return {"texto_extraido": result}
