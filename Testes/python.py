from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.mgmt.web import WebSiteManagementClient
from azure.mgmt.resource import ResourceManagementClient
from flask import Flask, jsonify, render_template, request
 
 
# Configuração da Aplicação Flask
app = Flask(__name__)
 
# Credenciais definidas diretamente no código
CONNECTION_STRING = ""
STORAGE_ACCOUNT_URL = ""
CONTAINER_NAME = ""
 
SUBSCRIPTION_ID = ""
RESOURCE_GROUP_NAME = ""
WEB_APP_NAME = ""
 
# Validação de configuração
if not STORAGE_ACCOUNT_URL or not CONTAINER_NAME:
    raise ValueError("As variáveis STORAGE_ACCOUNT_URL e CONTAINER_NAME devem estar configuradas.")
 
if not SUBSCRIPTION_ID or not RESOURCE_GROUP_NAME or not WEB_APP_NAME:
    raise ValueError("As variáveis SUBSCRIPTION_ID, RESOURCE_GROUP_NAME e WEB_APP_NAME devem estar configuradas.")
 
# Inicializar credenciais e clientes do Azure
credential = DefaultAzureCredential()
 
# Blob Service Client
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)
 
# Web Site Management Client
web_client = WebSiteManagementClient(credential, SUBSCRIPTION_ID)
 
 
@app.route("/list-blobs", methods=["GET"])
def list_blobs():
    try:
        blobs = container_client.list_blobs()
        blob_list = [blob.name for blob in blobs]
        return render_template("index.html", blobs=blob_list)
    except Exception as e:
        return render_template("index.html", error=f"Erro ao listar blobs: {e}")
   
    # Verificação inicial: listar blobs
print("Blobs no contêiner:")
for blob in container_client.list_blobs():
    print(blob.name)
   
 
# Baixar o blob para um arquivo local
blob_client = blob_service_client.get_blob_client(container="teste", blob="Teste.txt")
 
blob_data = blob_client.download_blob().readall()
print(blob_data.decode('utf-8'))
# Página inicial
@app.route("/")
def home():
    return render_template("index.html")  # Página de interação (opcional)
 
# Executar a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)
