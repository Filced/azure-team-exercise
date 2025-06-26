#import os
#account_key = os.environ.get("AZURE_ACC_KEY")
#if not account_key:
#   raise EnvironmentError(" AZURE_ACC_KEY är inte satt som miljövariabel.")

from azure.storage.blob import BlobServiceClient

account_key = open("azure.key").read().strip()
connection_string = f"DefaultEndpointsProtocol=https;AccountName=fdesa;AccountKey={account_key};EndpointSuffix=core.windows.net"

local_file = "rapport.txt"

container_name = "fdeblob"
blob_name = "rapport.txt"


blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

with open(local_file, "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print(" Filen har laddats upp till Azure Blob Storage!")
