import asyncio
import time
import os
import re
from netwatch.models import PingResult, Status

# Messages ping writes to stderr when a name can't be resolved (with LC_ALL=C)
DNS_ERROR_MESSAGES = (
    "Name or service not known",  # the name doesn't exist
    "Temporary failure in name resolution",  # no DNS server reachable
)


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


async def ping_many(hosts: list[str], timeout_s: int = 2) -> list[PingResult]:
    return await asyncio.gather(*(ping(host, timeout_s) for host in hosts))
