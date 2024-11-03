from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import requests
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

# Set up the Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

LUAS_PERSEGI_URL = "http://98.80.10.249:8080/function/luas-persegi"
LUAS_PERMUKAAN_KUBUS_URL = "http://52.90.249.200:8080/function/luas-permukaan-kubus"


# Models.
class LuasPersegi(BaseModel):
    rusuk: int


class LuasPermukaanKubus(BaseModel):
    rusuk: int


# Render the page with the form
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Endpoint for the first form, accepting JSON data
@app.post("/submit-form1/")
async def submit_form1(data: LuasPersegi):
    try:
        # Access JSON data with data.input_data1
        send_data = {"rusuk": data.rusuk}
        response = requests.post(LUAS_PERSEGI_URL, json=send_data)
        response_data = response.json()
        return JSONResponse(content={"success": True, "data": response_data})

    except requests.RequestException as e:
        print(f"Error with luas persegi submission: {e}")
        return JSONResponse(content={"success": False, "error": "Failed to submit data to luas persegi API"})


# Endpoint for the second form, accepting JSON data
@app.post("/submit-form2/")
async def submit_form2(data: LuasPermukaanKubus):
    try:
        # Access JSON data with data.input_data2
        send_data = {"rusuk": data.rusuk}
        response = requests.post(LUAS_PERMUKAAN_KUBUS_URL, json=send_data)
        response_data = response.json()
        return JSONResponse(content={"success": True, "data": response_data})

    except requests.RequestException as e:
        print(f"Error with luas permukaan kubus submission: {e}")
        return JSONResponse(content={"success": False, "error": "Failed to submit data to luas permukaan kubus API"})


# Test endpoint and models.
@app.post("/luas-persegi/")
async def luas_persegi(luas_persegi: LuasPersegi):
    luas = luas_persegi.rusuk ** 2

    return JSONResponse(content={"success": True, "luas": luas})


@app.post("/luas-permukaan-kubus/")
async def luas_permukaan_kubus(luas_permukaan_kubus: LuasPermukaanKubus):
    # response = requests.post(
    #     f"http://{LUAS_PERSEGI_URL}/function/luas-persegi",
    #     luas_permukaan_kubus
    # )
    response = requests.post(
        LUAS_PERSEGI_URL,
        {"rusuk": luas_permukaan_kubus.rusuk}
    )

    data = response.json()

    luas_permukaan = data["luas"] * 6

    return JSONResponse(content={"success": True, "luas_permukaan": luas_permukaan})
