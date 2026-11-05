import json
import os
from datetime import datetime
from src.hasher import calculate_sha256

def generate_baseline(directory: str, output_file: str = "baseline.json")->dict:
    baseline_records = {}
    abs_dir = os.path.abspath(directory)

    print(f"[*] Generating baseline for: {abs_dir}")
    for root, _, files in os.walk(abs_dir):
        for filename in files:
            full_path = os.path.join(root, filename)
            file_hash = calculate_sha256(full_path)
            if file_hash:
                baseline_records[full_path] = file_hash

    payload ={
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "target_directory": abs_dir,
        "total_files": len(baseline_records),
        "hashes": baseline_records

    }

    with open(output_file, "w") as f:
        json.dump(payload, f, indent=4)
        print(f"[+] Baseline saved to '{output_file}' with {len(baseline_records)} indexed files.")
    return payload
if  __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "test_dir"
    generate_baseline(target)
