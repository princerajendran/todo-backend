import jwt
from datetime import datetime, timedelta

# Stage 1: Generate the JWT Token
def generate_token():
    # Payload with 'sub' as a string
    payload = {
        "sub": str(1),  # Convert user ID to string
        "exp": datetime.utcnow() + timedelta(hours=1)  # Optional: Add expiration
    }

    # Secret key for encoding
    secret_key = "kROyqhkESBvw9sOAupyUEOuoCP3dPl0s7CFLW3fLKkOpPWzabHd9mH6hVPkPcRLH"

    # Generate the token
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("Generated Token:", token)
    return token

# Stage 2: Decode the JWT Token
def decode_token(token):
    # Secret key for decoding (must match the one used for encoding)
    secret_key = "kROyqhkESBvw9sOAupyUEOuoCP3dPl0s7CFLW3fLKkOpPWzabHd9mH6hVPkPcRLH"

    try:
        # Decode the token
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        print("Decoded Payload:", payload)
    except jwt.ExpiredSignatureError:
        print("Error: Token has expired.")
    except jwt.InvalidTokenError as e:
        print("Invalid Token:", e)

# Stage 3: Combine and Run
if __name__ == "__main__":
    print("=== Stage 1: Token Generation ===")
    token = generate_token()

    print("\n=== Stage 2: Token Decoding ===")
    decode_token(token)