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
    
    file_path = "sample_erg_screen.jpeg"
    image_name = "sample_erg_18_04_24.jpg"
    
    with open(file_path, "rb") as data:
        container_client.upload_blob(name=image_name, data=data)
        print(f"Image '{image_name}' uploaded successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
