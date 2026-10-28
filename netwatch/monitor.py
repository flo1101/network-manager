import time
import asyncio

from netwatch.models import Status
from netwatch.checks.ping import ping_many


async def print_host_state(host: str, msg: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{timestamp} {host} {msg}")


async def monitor(targets: list[str], interval_s: int = 5) -> None:
    last_status: dict[str, Status] = {}
    changed_at: dict[str, float] = {}

    while True:
        results = await ping_many(targets)
        for r in results:
            prev = last_status.get(r.host)
            if prev is None:
                await print_host_state(r.host, f"initial: {r.status.value}")
                last_status[r.host] = r.status
                changed_at[r.host] = time.monotonic()
                continue
            if r.status != prev:
                msg = f"{prev.value} -> {r.status.value}"
                if r.status == Status.UP:
                    msg += f" (down for {time.monotonic() - changed_at[r.host]:.1f} s)"
                await print_host_state(r.host, msg)
                last_status[r.host] = r.status
                changed_at[r.host] = time.monotonic()
        await asyncio.sleep(5)
