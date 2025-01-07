from fastapi import FastAPI
import uvicorn
from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from fastapi.responses import StreamingResponse
from typing import List
import os
from io import BytesIO

app = FastAPI()

def get_blob_service_client(tenant_id: str, client_id: str, client_secret: str, storage_account_name: str):
    try:
        # Authenticate with Azure using service principal credentials
        credential = ClientSecretCredential(
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret
        )
        # Create BlobServiceClient using the storage account name and credentials
        blob_service_client = BlobServiceClient(
            account_url=f"https://{storage_account_name}.blob.core.windows.net",
            credential=credential
        )
        return blob_service_client
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/containers")
async def list_containers(
    tenant_id: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...),
    storage_account_name: str = Form(...)
) -> List[str]:
    try:
        # Get BlobServiceClient
        blob_service_client = get_blob_service_client(tenant_id, client_id, client_secret, storage_account_name)
        # List all containers
        containers = blob_service_client.list_containers()
        container_names = [container.name for container in containers]
        return container_names
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return "Hello World!!"
