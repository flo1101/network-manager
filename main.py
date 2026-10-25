import re
import os
import time
import asyncio
from dataclasses import dataclass
from enum import Enum

# Messages ping writes to stderr when a name can't be resolved (with LC_ALL=C)
DNS_ERROR_MESSAGES = (
    "Name or service not known",  # the name doesn't exist
    "Temporary failure in name resolution",  # no DNS server reachable
)


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
    duration: float | None = None


async def sequential_ping(hosts: list[str], timeout_s: int = 2) -> list[PingResult]:
    results: list[PingResult] = []
    for h in hosts:
        result = await ping(h, timeout_s)
        results.append(result)
    return results


async def async_ping(hosts: list[str], timeout_s: int = 2) -> list[PingResult]:
    return await asyncio.gather(*(ping(host, timeout_s) for host in hosts))


async def ping(host: str, timeout_s: int = 2) -> PingResult:
    t0 = time.perf_counter()
    cmd = ["ping", "-c", "1", "-W", str(timeout_s), host]
    env = {**os.environ, "LC_ALL": "C"}  # force english output
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,  # capture stdout
        stderr=asyncio.subprocess.PIPE,  # capture stderr
        env=env,
    )
    stdout_bytes, stderr_bytes = await proc.communicate()

    stdout = stdout_bytes.decode()
    stderr = stderr_bytes.decode()
    returncode = proc.returncode

    duration = time.perf_counter() - t0
    results = parse_ping(host, returncode, stdout, stderr, duration)
    return results


def parse_ping(
    host: str, returncode: int | None, stdout: str, stderr: str, duration: float
) -> PingResult:
    if returncode is None:
        return PingResult(host=host, status=Status.ERROR, duration=duration)
    # Success
    if returncode == 0:
        match = re.search(r"time=([\d.]+)", stdout)
        if match:
            return PingResult(
                host=host,
                status=Status.UP,
                rtt_ms=float(match.group(1)),
                duration=duration,
            )
    # Timeout
    if returncode == 1:
        return PingResult(host=host, status=Status.TIMEOUT, duration=duration)
    # DNS error
    if any(msg in stderr for msg in DNS_ERROR_MESSAGES):
        return PingResult(host=host, status=Status.DNS_ERROR, duration=duration)
    # Any other error
    return PingResult(host=host, status=Status.ERROR, duration=duration)


def print_ping_results(results: list[PingResult], elapsed: float) -> None:
    print(f"Elapsed time: {elapsed:.3f} seconds")
    for r in results:
        print(f"{r.host}: {r.status.value}", end="")
        if r.rtt_ms is not None:
            print(f" (RTT: {r.rtt_ms} ms)", end="")
        if r.ttl is not None:
            print(f" (TTL: {r.ttl})", end="")
        print()


async def main() -> None:
    targets: list[str] = [
        "192.168.0.1",  # router
        "1.1.1.1",  # cloudflare
        "google.com",  # google.com
        "doesnotexist.invalid",
        "10.255.255.1",  # private network adress (unreachable)
        "10.255.255.2",
        "10.255.255.3",
        "10.255.255.4",
    ]
    t0_async = time.perf_counter()
    results_async = await async_ping(targets)
    elapsed_async = time.perf_counter() - t0_async

    t0_seq = time.perf_counter()
    results_seq = await sequential_ping(targets)
    elapsed_seq = time.perf_counter() - t0_seq

    print("\nAsync ping results:")
    print_ping_results(results_async, elapsed_async)

    print("\nSequential ping results:")
    print_ping_results(results_seq, elapsed_seq)


if __name__ == "__main__":
    asyncio.run(main())
