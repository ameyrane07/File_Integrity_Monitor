import re
from collections import defaultdict

FAILED_AUTH_PATTERN = re.compile(
    r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)

def parse_auth_log(log_path: str, threshold: int = 3) -> dict:
    """Parses an auth log file and detects brute-force attack patterns."""
    failed_attempts = defaultdict(lambda: {"count": 0, "users": set()})

    try:
        with open(log_path, "r") as f:
            for line in f:
                match = FAILED_AUTH_PATTERN.search(line)
                if match:
                    user = match.group("user")
                    ip = match.group("ip")
                    failed_attempts[ip]["count"] += 1
                    failed_attempts[ip]["users"].add(user)
    except FileNotFoundError:
        print(f"[-] Log file '{log_path}' not found.")
        return {}

    brute_force_alerts = {}
    print(f"\n--- Authentication Log Analysis Report ({log_path}) ---")
    for ip, data in failed_attempts.items():
        is_suspicious = data["count"] >= threshold
        status = "ALERT: BRUTE-FORCE DETECTED" if is_suspicious else "NORMAL"
        print(f"IP: {ip:<16} Failures: {data['count']:<4} Users: {list(data['users'])} [{status}]")
        if is_suspicious:
            brute_force_alerts[ip] = {
                "failures": data["count"],
                "targeted_users": list(data["users"])
            }

    return brute_force_alerts

if __name__ == "__main__":
    import sys
    log_file = sys.argv[1] if len(sys.argv) > 1 else "sample_auth.log"
    parse_auth_log(log_file)
