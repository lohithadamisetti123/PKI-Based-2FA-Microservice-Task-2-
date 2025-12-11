import os
import base64
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import pyotp
import time

app = FastAPI()

DATA_DIR = "data"
SEED_FILE = os.path.join(DATA_DIR, "seed.txt")
PRIVATE_KEY_FILE = "student_private.pem"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


class DecryptSeedRequest(BaseModel):
    encrypted_seed: str


class Verify2FARequest(BaseModel):
    code: str


# ---------- Decrypt Seed Endpoint ----------
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: DecryptSeedRequest):
    encrypted_b64 = req.encrypted_seed
    try:
        encrypted_bytes = base64.b64decode(encrypted_b64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid Base64 input")

    try:
        with open(PRIVATE_KEY_FILE, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )

        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        hex_seed = decrypted_bytes.decode().strip()
        if len(hex_seed) != 64 or not all(c in "0123456789abcdef" for c in hex_seed.lower()):
            raise ValueError("Decrypted seed invalid")

        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)

        return {"status": "ok"}

    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")


# ---------- Generate TOTP Endpoint ----------
@app.get("/generate-2fa")
def generate_2fa_endpoint():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    seed_bytes = bytes.fromhex(hex_seed)
    seed_b32 = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(seed_b32, digits=6, interval=30)
    code = totp.now()
    remaining = 30 - (int(time.time()) % 30)
    return {"code": code, "valid_for": remaining}


# ---------- Verify TOTP Endpoint ----------
@app.post("/verify-2fa")
def verify_2fa_endpoint(req: Verify2FARequest):
    if not req.code:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    seed_bytes = bytes.fromhex(hex_seed)
    seed_b32 = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(seed_b32, digits=6, interval=30)
    valid = totp.verify(req.code, valid_window=1)
    return {"valid": valid}


# ---------- Run FastAPI ----------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
