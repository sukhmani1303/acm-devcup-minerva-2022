#Importing the libraries
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import keras
from fastapi.staticfiles import StaticFiles

app = FastAPI() 

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("message.html", {"request": request})

def rfai(data) -> np.ndarray:
    imgg = np.array(Image.open(BytesIO(data)))
    return imgg

@app.post("/action", response_class=HTMLResponse)
async def u_name(request: Request, uname : UploadFile = File(...)):

    imh1 = rfai(await uname.read())
    cv2.imwrite('static/chest_x_ray.png',imh1) 
    imh1 = np.array(imh1)/255
    imh2 = cv2.resize(imh1, (180, 180))
    imh_new = np.repeat(imh2[..., np.newaxis], 3, -1)
    imh_new =np.expand_dims(imh_new, 0)
    m2 = keras.models.load_model('inception.h5')
    yp_test = m2.predict(imh_new)
    result = ""

    print(yp_test)
    if yp_test > 0.5:
        result = "Pneumonia Positive"
    else:
        result = "Pneumonia Negative"

    return templates.TemplateResponse("scr2.html", {"request": request, "res": result, "acc" : round(yp_test[0][0]*100,2)})

if __name__ == '__main__':
    uvicorn.run(app,host = '127.0.0.1', port = 8000)
