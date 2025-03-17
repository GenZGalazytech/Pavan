from fastapi.middleware.cors import CORSMiddleware
import connect
from Routes.routes import router
from fastapi import FastAPI, Form, UploadFile, File
from datetime import datetime
from typing import List
from connect import get_image_collection
from Controllers.modelcontroller import image_processing
import io
from PIL import Image
from connect import image_collection,blob_service_client,CONTAINER_NAME
from models.models import Message


collection=get_image_collection()

app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.on_event("startup")
# async def startup_event():
#     try:
#         connect_to_db()
#     except Exception as e:
#         print(e)

@app.get('/')
async def index():
    return {"Backend Working...!!"}


@app.post("/upload")
async def upload_images(
    event_name: str = Form(...),
    event_date: str = Form(...),
    username: str = Form(...),
    files: List[UploadFile] = File(...)
):
    image_docs = []

    for file in files:
        # Convert UploadFile to PIL Image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")  # Convert to RGB PIL image
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
        blob_client.upload_blob(image_bytes, overwrite=True)

        embeddings = image_processing(image)

         # Generate Image URL
        image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{file.filename}"

        
        image_docs.append({
                "username": username,
                "filename": file.filename,
                "content_type": file.content_type,
                "image_url": image_url,
                "event_name": event_name,
                "event_date": event_date,
                "embeddings": embeddings
            })

    if image_docs:
        image_collection.insert_many(image_docs)
        return {"message": f"{len(image_docs)} images uploaded successfully!"}

    return {"error": "No images received!"}



# @app.post('/chat')
# def chat_bot(message : Message):
#     return {"reply" :f"hey {message.message}"}

app.include_router(router,prefix="/user") 