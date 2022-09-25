#Importing the libraries
from webbrowser import get
from fastapi import FastAPI, Request, Body, File, UploadFile, Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from PIL import Image
from io import BytesIO
import numpy as np
import cv2

# import multipart

app = FastAPI() #created an obj

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

def to_arr(data) -> np.ndarray:
    imgg = np.array(Image.open(BytesIO(data)))
    return imgg

@app.post("/action")
async def u_name(uname : UploadFile = File(...)):

    print("hello")
    imh = to_arr(await uname.read())
    # print(type(BytesIO(await uname.read())))
    
    fixed_imh = cv2.cvtColor(imh, cv2.COLOR_BGR2RGB)
    cv2.imshow("yy",fixed_imh)
    
    # waits for user to press any key
    # (this is necessary to avoid Python kernel form crashing)
    cv2.waitKey(0)
    return
    # response1 = RedirectResponse(url='/min')
    # return asd, image11


@app.post('/min', response_class=HTMLResponse)
def home111(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("pp.html", {"request": request, "data": data})

if __name__ == '__main__':
    uvicorn.run(app,host = '127.0.0.1', port = 8000)
