from json import dumps
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
import uvicorn
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
	title="budget-tracker",
	version=1.1,
	description="api for budget-tracker",
	redoc_url=None,
	openapi_url=None
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/app", StaticFiles(directory="app",html=True), name="app")

# Health
@app.get("/health")
async def health():
	return {"message": app.title+" "+str(app.version)+" Alive"}

# Execute on startup
@app.on_event("startup")
async def startup_event():
	print("App started")

# Execute on shutdown
@app.on_event("shutdown")
async def shutdown_event():
	print("App stopped")


ws = uvicorn.Server(
	config = uvicorn.Config(
		app=app,
		port=8000,
		host="0.0.0.0",
		log_level="info",
		log_config={
			"version": 1,
			"disable_existing_loggers": False,
		}
	)
)

if __name__ == "__main__":
	uvicorn.run("main:app",host='0.0.0.0', port=8000, reload=True)