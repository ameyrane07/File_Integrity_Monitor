import json
import os
from src.hasher import calculate_sha256

def verify_integrity(baseline_path: str = "baseline.json") -> dict:
    if not os.path.exists(baseline_path):
        print(f"[-] Error: Baseline file '{baseline_path}' not found.")
        return {}

    with open(baseline_path, "r") as f:
        baseline_data = json.load(f)

    baseline_hashes = baseline_data.get("hashes", {})
    target_dir = baseline_data.get("target_directory")

    if not target_dir or not os.path.exists(target_dir):
        print(f"[-] Target directory '{target_dir}' does not exist.")
        return {}

    current_files = {}
    for root, _, files in os.walk(target_dir):
        for filename in files:
            full_path = os.path.join(root, filename)
            h = calculate_sha256(full_path)
            if h:
                current_files[full_path] = h

    baseline_set = set(baseline_hashes.keys())
    current_set = set(current_files.keys())

    new_files = list(current_set - baseline_set)
    deleted_files = list(baseline_set - current_set)
    modified_files = [
        f for f in (baseline_set & current_set)
        if baseline_hashes[f] != current_files[f]
    ]

    print("\n--- Integrity Verification Report ---")
    print(f"Target Directory: {target_dir}")
    print(f"Status: {'ANOMALIES DETECTED' if (new_files or deleted_files or modified_files) else 'CLEAN'}")
    
    if modified_files:
        print("\n[!] MODIFIED FILES:")
        for f in modified_files:
            print(f"    - {f}")
    if new_files:
        print("\n[!] NEW / UNINDEXED FILES:")
        for f in new_files:
            print(f"    + {f}")
    if deleted_files:
        print("\n[!] DELETED FILES:")
        for f in deleted_files:
            print(f"    x {f}")

    return {
        "modified": modified_files,
        "new": new_files,
        "deleted": deleted_files
    }

if __name__ == "__main__":
    verify_integrity()
