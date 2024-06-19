from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

load_dotenv()

connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

if not connection_string:
    raise ValueError("Missing Azure storage connection string in environment variables")

try:
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    container_client = blob_service_client.get_container_client('ergscreens')
    
    blobs = container_client.list_blobs()
    blobs_list = list(blobs)
    
    if blobs_list is not None:
        print("Connection successful, able to access container and list blobs.")
    else:
        print("Connection successful, but no blobs found in the container.")

except Exception as e:
    print(f"An error occurred: {e}")
