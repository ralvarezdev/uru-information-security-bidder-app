# uru-information-security-bidder-app

**Note:** This repository is archived and read-only.

Bidder (encrypter) client, in Python and Streamlit.

Part of a set of Information Security college course (URU) projects forming a secure tender (bid) file submission system, all under `ralvarezdev`:

- **`uru-information-security-certificate-grpc`** — certificate authority gRPC service (port 50053)
- **`uru-information-security-encrypter-grpc`** — encrypts and signs bidder files, forwards them to the decrypter (50051)
- **`uru-information-security-decrypter-grpc`** — receives, stores and decrypts files for the tender owner (50052)
- **`uru-information-security-certificate-app`**, **`-bidder-app`**, **`-admin-app`** — Streamlit UIs to request certificates, submit files and manage files (8503, 8502, 8501)

## What it does

Streamlit UI "Bidder Client: Secure File Submission". The bidder selects a PDF or Word (.docx) file and uploads their digital certificate (.txt or .pem); the file is streamed in chunks to the Encrypter gRPC service, which encrypts, signs and forwards it.

## Project structure

- **`main.py`** — Streamlit app
- **`microservice/grpc/`** — gRPC client; **`ralvarezdev/`** — generated stubs
- **`encrypter-grpc`** — git submodule (see `.gitmodules`) with the service's proto definitions
- **`Dockerfile`** — runs Streamlit on port 8502; `compile_proto.bat` and `update_submodules.bat` are Windows helpers

## Configuration and running

Environment variables (via git-ignored `.env`): `ENCRYPTER_GRPC_HOST`, `ENCRYPTER_GRPC_PORT`.

```bash
git submodule update --init
pip install -r requirements.txt    # may be UTF-16 encoded; convert if pip complains
streamlit run main.py --server.port=8502
```

## License

GNU General Public License v3.0 (see `LICENSE`).
