from enum import Enum
from dataclasses import dataclass


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
