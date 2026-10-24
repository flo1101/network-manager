import re
import subprocess


def ping(host: str, timeout_s: int = 2) -> float | None:
    cmd = ["ping", "-c", "1", "-W", str(timeout_s), host]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # print("ping output:", result.stdout)
    match = re.search(r"time=([\d.]+)", result.stdout)
    if match:
        return float(match.group(1))
    return None


if __name__ == "__main__":
    targets: list[str] = [
        "192.168.0.1",  # this machine
        "1.1.1.1",  # cloudflare
        "google.com",  # google.com
        "10.255.255.1",  # private network adress (unreachable)
        "doesnotexist.invalid",
    ]
    for host in targets:
        rtt = ping(host)
        print(f"{host:<22} {rtt} ms" if rtt is not None else f"{host:<22} unreachable")
