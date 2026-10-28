import asyncio

from netwatch.monitor import monitor


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

    await monitor(targets, interval_s=5)


if __name__ == "__main__":
    asyncio.run(main())
