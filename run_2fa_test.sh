#!/bin/bash

echo "🚀 Starting FastAPI server..."
# Start FastAPI in background
uvicorn main:app --reload &
SERVER_PID=$!

# Give server a moment to start
sleep 3

# -------------------------
# Prepare encrypted seed Base64
# -------------------------
if [ -f "encrypted_seed.bin" ]; then
    ENCRYPTED_B64=$(base64 -w 0 encrypted_seed.bin)
else
    echo "❌ encrypted_seed.bin not found"
    kill $SERVER_PID
    exit 1
fi

# -------------------------
# Decrypt Seed via API
# -------------------------
echo "🔐 Decrypting seed..."
DECRYPT_RESPONSE=$(curl -s -X POST "http://127.0.0.1:8000/decrypt-seed" \
    -H "Content-Type: application/json" \
    -d "{\"encrypted_seed\":\"$ENCRYPTED_B64\"}")

echo "Decryption Response: $DECRYPT_RESPONSE"

# -------------------------
# Generate TOTP via API
# -------------------------
echo "🔑 Generating TOTP..."
TOTP_RESPONSE=$(curl -s -X GET "http://127.0.0.1:8000/generate-2fa")
echo "TOTP Response: $TOTP_RESPONSE"

# Extract TOTP code for verification
TOTP_CODE=$(echo $TOTP_RESPONSE | python -c "import sys, json; print(json.load(sys.stdin)['code'])")

# -------------------------
# Verify TOTP via API
# -------------------------
echo "✅ Verifying TOTP code: $TOTP_CODE"
VERIFY_RESPONSE=$(curl -s -X POST "http://127.0.0.1:8000/verify-2fa" \
    -H "Content-Type: application/json" \
    -d "{\"code\":\"$TOTP_CODE\"}")
echo "Verification Response: $VERIFY_RESPONSE"

# -------------------------
# Stop FastAPI server
# -------------------------
echo "🛑 Stopping FastAPI server..."
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null

echo "Done."
