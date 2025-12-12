#!/usr/bin/env python3
"""
generate_commit_proof.py

Signs the latest commit hash using student_private.pem (RSA-PSS SHA256),
encrypts the signature with instructor_public.pem (RSA-OAEP SHA256),
and prints + writes the base64-encoded encrypted signature.

Outputs:
 - Commit Hash: <40-hex>
 - Encrypted Signature (base64): <single-line>
 - Writes commit_proof.b64 in repo root
"""

import os
import sys
import subprocess
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
STUDENT_PRIV = os.path.join(REPO_ROOT, "student_private.pem")
INSTRUCTOR_PUB = os.path.join(REPO_ROOT, "instructor_public.pem")
OUT_B64 = os.path.join(REPO_ROOT, "commit_proof.b64")


def get_commit_hash():
    try:
        out = subprocess.check_output(["git", "log", "-1", "--format=%H"], cwd=REPO_ROOT)
    except subprocess.CalledProcessError as e:
        print("ERROR: git command failed:", e, file=sys.stderr)
        sys.exit(1)
    commit = out.decode().strip()
    if len(commit) != 40 or not all(c in "0123456789abcdef" for c in commit.lower()):
        print("ERROR: commit hash is not a 40-character hex string:", commit, file=sys.stderr)
        sys.exit(1)
    return commit


def load_private_key(path):
    if not os.path.isfile(path):
        print(f"ERROR: private key not found at {path}", file=sys.stderr); sys.exit(1)
    with open(path, "rb") as f:
        data = f.read()
    try:
        key = serialization.load_pem_private_key(data, password=None)
    except Exception as e:
        print("ERROR: failed to load private key:", e, file=sys.stderr); sys.exit(1)
    return key


def load_public_key(path):
    if not os.path.isfile(path):
        print(f"ERROR: public key not found at {path}", file=sys.stderr); sys.exit(1)
    with open(path, "rb") as f:
        data = f.read()
    try:
        key = serialization.load_pem_public_key(data)
    except Exception as e:
        print("ERROR: failed to load public key:", e, file=sys.stderr); sys.exit(1)
    return key


def sign_message(message: str, private_key) -> bytes:
    """
    Sign a message using RSA-PSS with SHA-256 and salt length = MAX.
    message: ASCII string (commit hash)
    returns: signature bytes
    """
    msg_bytes = message.encode("utf-8")  # CRITICAL: ASCII/UTF-8 bytes of commit hash
    signature = private_key.sign(
        msg_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """
    Encrypt data using RSA-OAEP with SHA-256 and MGF1(SHA256).
    returns: ciphertext bytes
    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def main():
    commit = get_commit_hash()
    print("Commit Hash:", commit)

    priv = load_private_key(STUDENT_PRIV)
    pub = load_public_key(INSTRUCTOR_PUB)

    # Sign
    sig = sign_message(commit, priv)
    # Encrypt
    encrypted = encrypt_with_public_key(sig, pub)
    # Base64 encode (single line)
    b64 = base64.b64encode(encrypted).decode("ascii")

    print("\nEncrypted Signature (base64):")
    print(b64)
    # Save
    with open(OUT_B64, "w") as f:
        f.write(b64 + "\n")
    print(f"\nSaved to: {OUT_B64}")


if __name__ == "__main__":
    main()
