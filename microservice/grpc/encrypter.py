import grpc

import ralvarezdev.encrypter_pb2_grpc as encrypter_pb2_grpc

def create_grpc_client(host: str, port: int):
    """
    Creates and returns a gRPC client stub.

	Args:
		host (str): The server host.
		port (int): The server port.

	Returns:
		encrypter_pb2_grpc.EncrypterStub: The gRPC client stub.
    """
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = encrypter_pb2_grpc.EncrypterStub(channel)
    return stub