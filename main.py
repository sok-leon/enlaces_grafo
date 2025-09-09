from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import ping_check  # importa tu script

app = FastAPI()

# Sirve archivos estáticos para el mapa
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/status")
async def status():
    # results = [
    #             {"name": "Sitio A - México", "ip": "8.8.8.8", "lat": 19.4326, "lng": -99.1332, "status": "UP"},
    #             {"name": "Sitio B - España", "ip": "1.1.1.1", "lat": 40.4168, "lng": -3.7038, "status": "down"}
    #         ]
    results = ping_check.get_json_status()   # llamamos la función de tu script
    return JSONResponse(results)

