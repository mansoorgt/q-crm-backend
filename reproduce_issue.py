import hashlib
from passlib.context import CryptContext
import sys

# Setup context as in the app
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

password = "test_password"
print(f"Original password: {password}")

# Reproduce the logic
sha256_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
print(f"SHA256 Hex Digest: {sha256_password}")
print(f"Length of Hex Digest: {len(sha256_password)}")

try:
    hashed = pwd_context.hash(sha256_password)
    print(f"Hashed Successfully: {hashed}")
except Exception as e:
    print(f"Error Hashing: {e}")
    import traceback
    traceback.print_exc()

# Check verify as well
try:
    verify = pwd_context.verify(sha256_password, hashed)
    print(f"Verify Result: {verify}")
except Exception as e:
    print(f"Error Verifying: {e}")
