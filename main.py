import base64
import io
import zipfile

import streamlit as st
import grpc

from microservice.grpc import (
	ENCRYPTER_GRPC_HOST,
	ENCRYPTER_GRPC_PORT
)
from microservice.grpc.encrypter import create_grpc_client
from ralvarezdev import encrypter_pb2, encrypter_pb2_grpc

# UI
st.title("Bidder Client: Secure File Submission")
st.markdown("Upload your File in **.pdf** or **.docx** format and your digital certificate **.txt** or **.pem** for a secure transmission.")

# gRPC Client Setup
try:
    stub = create_grpc_client(ENCRYPTER_GRPC_HOST, ENCRYPTER_GRPC_PORT)
except Exception as e:
    st.error(f"Could not connect to gRPC server: {e}")
    st.stop()

# File Upload
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("1. Select your File (PDF or Word)", type=['pdf', 'docx'])
with col2:
    uploaded_certificate = st.file_uploader("2. Upload your digital certificate (.txt or .pem)", type=["txt", "pem"])

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])
with button_col2:
    if st.button("Send Signed & Encrypted File", type="primary"):
        if uploaded_file is not None and uploaded_certificate is not None:
            filename = uploaded_file.name
            certificate_bytes = uploaded_certificate.getvalue()

            # Compress the file into a .zip in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.writestr(filename, uploaded_file.getvalue())
            zip_bytes = zip_buffer.getvalue()
            zip_filename = filename + ".zip" if not filename.endswith(".zip") else filename

            # Metadata: attach certificate as base64-encoded string
            certificate_bytes = uploaded_certificate.getvalue()
            certificate_b64 = base64.b64encode(certificate_bytes).decode(
	            'ascii'
	            )
            metadata = [('certificate', certificate_b64)]
            CHUNK_SIZE = 1024 * 1024  # 1 MB

            def generate_chunks(filename: str, data: bytes):
                for i in range(0, len(data), CHUNK_SIZE):
                    chunk = data[i:i + CHUNK_SIZE]
                    yield encrypter_pb2.SendEncryptFileRequest(content=chunk, filename=filename)

            try:
                with st.spinner(f"Securely sending '{zip_filename}'..."):
                    request_iterator = generate_chunks(zip_filename, zip_bytes)
                    stub.SendEncryptedFile(request_iterator, metadata=metadata)

                st.success(f"'{zip_filename}' has been successfully sent!")
                st.info("Your file was compressed, signed with the provided certificate, and encrypted on the server.")
                st.balloons()
            except grpc.RpcError as e:
                st.error(f"Error while sending file: {e.details()}")
                st.error("Please ensure your certificate is valid and registered.")
        else:
            st.warning("Please select both the proposal file and your digital certificate.")
