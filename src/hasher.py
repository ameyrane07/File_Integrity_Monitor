import hashlib
import os
from typing import Optional

CHUNK_SIZE = 65536

def calculate_sha256(filepath: str) -> Optional[str]:
    if not os.path.isfile(filepath):
         return None

    digest = hashlib.sha256()
    try:
           with open(filepath, "rb") as stream:
               while chunk := stream.read(CHUNK_SIZE):
                   digest.update(chunk)
           return digest.hexdigest()
    except (PermissionError, OSError) as err:
        print(f"[!] Access error on {filepath}: {err}")

        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 src/hasher.py <filepath>")
        sys.exit(1)
    target = sys.argv[1]
    res = calculate_sha256(target)
    if res:
        print(f"[+] SHA-256 ({target}):\n   {res}")
    else:
        print(f"[-] Could not hash target: {target}")
