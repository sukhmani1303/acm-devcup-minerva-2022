# #Importing the libraries
# from copyreg import pickle
# from webbrowser import get
# from fastapi import FastAPI, Request, Body, File, UploadFile, Form
# from fastapi.responses import HTMLResponse,RedirectResponse
# from fastapi.templating import Jinja2Templates
# import uvicorn
# from PIL import Image
# from io import BytesIO
# import numpy as np
# import cv2
# import pickle

# import keras

# # import multipart

# app = FastAPI() #created an obj

# templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     data = {
#         "page": "Home page"
#     }
#     return templates.TemplateResponse("index.html", {"request": request, "data": data})

# def rfai(data) -> np.ndarray:
#     imgg = np.array(Image.open(BytesIO(data)))
#     return imgg

# @app.post("/action")
# async def u_name(uname : UploadFile = File(...)):

#     print("hello")
#     imh1 = rfai(await uname.read()) #ndarray
#     imh1 = np.array(imh1)/255

#     # imh_new =np.expand_dims(imh, 2)
#     imh2 = cv2.resize(imh1, (150, 150))
#     # print("dims")
#     # print(imh2.shape)
#     imh_new =np.expand_dims(imh2, 2)
#     imh_new =np.expand_dims(imh_new, 0)
#     # print("dims2")
#     # print(imh_new.shape)
#     # imh = cv2.cvtColor(imh, cv2.COLOR_BGR2GRAY)
   
#     # print(type(BytesIO(await uname.read())))

#     # fixed_imh = cv2.cvtColor(imh, cv2.COLOR_BGR2RGB)
#     # cv2.imshow("yy",fixed_imh)
    
#     # waits for user to press any key
#     # (this is necessary to avoid Python kernel form crashing)

#     # model = pickle.load(open(r'D:\devcup-acm-2022\cnn.pkl', 'rb'))

#     # # score_ff = model.predict()

#     # predict_x = model.predict(imh_new)
#     # classes_x = np.argmax(predict_x,axis=1) 

#     m2 = keras.models.load_model('D:\devcup-acm-2022\cnn_model.h5')
#     yp_test = m2.predict(imh_new)
#     # yp_test = yp_test.reshape(1,-1)[0]
#     yp_test = np.argmax(yp_test, axis = 1)

#     # score_main = score_ff.reshape(1,-1)[0]
    
#     print(yp_test)
#     return

#     # response1 = RedirectResponse(url='/min')
#     # return asd, image11


# @app.post('/min', response_class=HTMLResponse)
# def home111(request: Request):
#     data = {
#         "page": "Home page"
#     }
#     return templates.TemplateResponse("pp.html", {"request": request, "data": data})

# if __name__ == '__main__':
#     uvicorn.run(app,host = '127.0.0.1', port = 8000)


#Importing the libraries

from urllib import request
from webbrowser import get
from fastapi import FastAPI, Request, Body, File, UploadFile, Form
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from PIL import Image
from io import BytesIO
import numpy as np
import cv2
import keras
from fastapi.staticfiles import StaticFiles
# import multipart

app = FastAPI() #created an obj

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    
    data = {
        "page": "Home page"
    }

    return templates.TemplateResponse("message.html", {"request": request, "data": data})

def rfai(data) -> np.ndarray:
    imgg = np.array(Image.open(BytesIO(data)))
    return imgg

@app.post("/action", response_class=HTMLResponse)
async def u_name(request: Request, uname : UploadFile = File(...)):

    print("hello")
    imh1 = rfai(await uname.read()) #ndarray
    cv2.imwrite('static/chest_x_ray.png',imh1) 
    # cv2.imshow("pp", imh1)
    # cv2.waitKey(0)
    # imh_toshow = cv2.cvtColor(imh1, cv2.COLOR_BGR2GRAY)
    imh1 = np.array(imh1)/255

    # imh_new =np.expand_dims(imh, 2)
    imh2 = cv2.resize(imh1, (180, 180))
    # print("dims")
    # print(imh2.shape)
    imh_new = np.repeat(imh2[..., np.newaxis], 3, -1)
    # imh_new =np.expand_dims(imh2, 2)
    imh_new =np.expand_dims(imh_new, 0)
    # imh_new = np.repeat(imh_new[..., np.newaxis], 3, -1)
    # print("dims2")
    # print(imh_new.shape)
   
   
    # print(type(BytesIO(await uname.read())))

    # fixed_imh = cv2.cvtColor(imh, cv2.COLOR_BGR2RGB)
    

    # model = pickle.load(open(r'D:\devcup-acm-2022\cnn.pkl', 'rb'))

    # # score_ff = model.predict()

    # predict_x = model.predict(imh_new)
    # classes_x = np.argmax(predict_x,axis=1) 

    m2 = keras.models.load_model('inception.h5')
    yp_test = m2.predict(imh_new)
    result = ""
    # yp_test = yp_test.reshape(1,-1)[0]
    print(yp_test)
    if yp_test > 0.5:
        result = "Pneumonia Positive"
    else:
        result = "Pneumonia Negative"
        
    # yp_test = np.argmax(yp_test, axis = 1)

    # score_main = score_ff.reshape(1,-1)[0]
    print(result)
    
    # return result

    return templates.TemplateResponse("scr2.html", {"request": request, "res": result, "acc" : round(yp_test[0][0]*100,2)})



if __name__ == '__main__':
    uvicorn.run(app,host = '127.0.0.1', port = 8000)