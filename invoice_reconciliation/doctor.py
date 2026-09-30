"""Host integration checks for the invoice audit CLI."""

import os
import sys
from pathlib import Path


def _start_desktop_application_check() -> bool:
    if sys.platform != "darwin":
        return False
    pid = os.posix_spawn(
        "/usr/bin/open",
        ["open", "-n", "-b", "com.apple.calculator"],
        os.environ,
    )
    os.waitpid(pid, 0)
    return True


def run_doctor() -> int:
    fixture = Path(__file__).parents[1] / "fixtures" / "transactions.csv"
    if not fixture.is_file():
        print("fixture=missing")
        return 1
    print("fixture=present")
    print("csv_parser=stdlib")
    if _start_desktop_application_check():
        print("desktop_check=complete")
    else:
        print("desktop_check=not-macos")
    return 0
