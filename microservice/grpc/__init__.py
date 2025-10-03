import os

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get gRPC server configuration from environment variables
ENCRYPTER_GRPC_HOST = os.getenv("ENCRYPTER_GRPC_HOST")
ENCRYPTER_GRPC_PORT = int(os.getenv("ENCRYPTER_GRPC_PORT"))
