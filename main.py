import re
import os
import subprocess
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    UP = "up"  # got a reply (exit code 0)
    TIMEOUT = "timeout"  # sent, but no reply  (exit code 1)
    DNS_ERROR = "dns_error"  # name could not be resolved (exit code 2)
    ERROR = "error"  # anything else


@dataclass
class PingResult:
    host: str
    status: Status
    rtt_ms: float | None = None
    ttl: int | None = None


def ping(host: str, timeout_s: int = 2) -> PingResult:
    cmd = ["ping", "-c", "1", "-W", str(timeout_s), host]
    env = {**os.environ, "LC_ALL": "C"}  # force english output language
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    # print(result.stdout)
    # Success
    if result.returncode == 0:
        match = re.search(r"time=([\d.]+)", result.stdout)
        if match:
            return PingResult(host=host, status=Status.UP, rtt_ms=float(match.group(1)))
    # Timeout
    if result.returncode == 1:
        return PingResult(host=host, status=Status.TIMEOUT)
    # DNS error
    match = re.search(r"not known", result.stderr)
    if match:
        return PingResult(host=host, status=Status.DNS_ERROR)
    # Any other error
    else:
        return PingResult(host=host, status=Status.ERROR)


if __name__ == "__main__":
    targets: list[str] = [
        "192.168.0.1",  # router
        "1.1.1.1",  # cloudflare
        "google.com",  # google.com
        "10.255.255.1",  # private network adress (unreachable)
        "doesnotexist.invalid",
    ]
    for host in targets:
        result: PingResult = ping(host)
        if result.status == Status.UP:
            print(f"{host:<22} {result.status} {result.rtt_ms} ms")
        else:
            print(f"{host:<22} {result.status}")
