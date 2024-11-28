import os
from flask import Flask, jsonify, render_template, request
from azure.storage.blob import BlobServiceClient

# Configuração da Aplicação Flask
app = Flask(__name__)

# Configuração de Conexão com Azure Storage
STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING") or "<sua-string-de-conexão>"
CONTAINER_NAME = "teste"

# Função para conectar ao serviço de blob
def connect_to_blob_service():
    try:
        blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)
        return blob_service_client
    except Exception as e:
        print(f"Erro ao conectar ao Azure Storage: {e}")
        return None

# Endpoint: Página inicial
@app.route("/")
def home():
    return render_template("index.html")  # Página HTML para interação (opcional)

# Endpoint: Listar blobs no container
@app.route("/list-blobs", methods=["GET"])
def list_blobs():
    blob_service_client = connect_to_blob_service()
    if not blob_service_client:
        return jsonify({"error": "Não foi possível conectar ao Azure Storage"}), 500
    
    try:
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blobs = container_client.list_blobs()
        blob_list = [{"name": blob.name, "size": blob.size, "last_modified": blob.last_modified} for blob in blobs]
        return jsonify(blob_list)  # Retorna a lista de blobs como JSON
    except Exception as e:
        return jsonify({"error": f"Erro ao listar blobs: {e}"}), 500

# Endpoint: Ler conteúdo de um blob específico
@app.route("/read-blob", methods=["GET"])
def read_blob():
    blob_name = request.args.get("blob_name")  # Nome do blob fornecido como parâmetro na URL
    if not blob_name:
        return jsonify({"error": "Parâmetro 'blob_name' é obrigatório"}), 400

    blob_service_client = connect_to_blob_service()
    if not blob_service_client:
        return jsonify({"error": "Não foi possível conectar ao Azure Storage"}), 500

    try:
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        blob_client = container_client.get_blob_client(blob_name)
        blob_data = blob_client.download_blob().readall()
        return jsonify({"blob_name": blob_name, "content": blob_data.decode("utf-8")})  # Retorna o conteúdo do blob
    except Exception as e:
        return jsonify({"error": f"Erro ao ler o blob '{blob_name}': {e}"}), 500

# Executar a aplicação Flask
if __name__ == "__main__":
    app.run(debug=True)

