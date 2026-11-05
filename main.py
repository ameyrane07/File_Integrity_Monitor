import argparse
import sys
from src.hasher import calculate_sha256
from src.baseline import generate_baseline
from src.detector import verify_integrity
from src.log_monitor import parse_auth_log

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive File Integrity & Security Monitoring System"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available modules")

    # Hash Command
    hash_parser = subparsers.add_parser("hash", help="Compute SHA-256 hash of a file")
    hash_parser.add_argument("file", help="Path to target file")

    # Baseline Command
    base_parser = subparsers.add_parser("baseline", help="Generate snapshot baseline")
    base_parser.add_argument("dir", help="Directory path to index")
    base_parser.add_argument("-o", "--output", default="baseline.json", help="Output baseline file")

    # Verify Command
    verify_parser = subparsers.add_parser("verify", help="Check directory integrity")
    verify_parser.add_argument("-b", "--baseline", default="baseline.json", help="Baseline path")

    # Log Monitor Command
    log_parser = subparsers.add_parser("logs", help="Analyze authentication logs")
    log_parser.add_argument("logfile", help="Path to auth log")
    log_parser.add_argument("-t", "--threshold", type=int, default=3, help="Alert threshold")

    args = parser.parse_args()

    if args.command == "hash":
        digest = calculate_sha256(args.file)
        if digest:
            print(f"[+] SHA-256 ({args.file}): {digest}")
    elif args.command == "baseline":
        generate_baseline(args.dir, args.output)
    elif args.command == "verify":
        verify_integrity(args.baseline)
    elif args.command == "logs":
        parse_auth_log(args.logfile, args.threshold)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
