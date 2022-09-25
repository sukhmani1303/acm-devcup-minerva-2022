#Importing the libraries
from webbrowser import get
from fastapi import FastAPI, Request, Body, File, UploadFile, Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from PIL import Image
from io import BytesIO
import numpy as np

# import multipart

app = FastAPI() #created an obj

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("index.html", {"request": request, "data": data})

def rfai(data) -> np.ndarray:
    imgg = np.array(Image.open(BytesIO(data)))
    return imgg

@app.post("/action")
async def u_name(uname : UploadFile = File(...)):

    # image = Image.open(uname.file)

    # asdasd111 = await uname.read()
    
    # image11 = Image.open(BytesIO(uname))

    qop = Image.open(uname)
    print(qop)
    print(uname.content_type)
    # response1 = RedirectResponse(url='/min')
    # return asd, image11

    return {"message": f"Successfully uploaded {file.filename}"}

@app.post('/min', response_class=HTMLResponse)
def home111(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("pp.html", {"request": request, "data": data})

if __name__ == '__main__':
    uvicorn.run(app,host = '127.0.0.1', port = 8000)
