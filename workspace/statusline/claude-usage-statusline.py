#!/usr/bin/python3
"""Persist only subscription counters for the existing host-side usage uploader."""

import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time


def snapshot_from_status(data):
    limits = data.get("rate_limits")
    if not isinstance(limits, dict):
        return None
    result = {}
    for source, target in (("five_hour", "5h"), ("seven_day", "7d")):
        value = limits.get(source)
        if not isinstance(value, dict):
            return None
        percent, resets = value.get("used_percentage"), value.get("resets_at")
        if (isinstance(percent, bool) or not isinstance(percent, (int, float))
                or not math.isfinite(percent) or not 0 <= percent <= 100
                or isinstance(resets, bool) or not isinstance(resets, (int, float))
                or not math.isfinite(resets) or resets <= time.time()):
            return None
        result[target] = {"pct": percent, "resets_at": int(resets)}
    return result


def write_snapshot(path, snapshot):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".usage-status-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as stream:
            json.dump(snapshot, stream)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        print("Claude")
        return
    snapshot = snapshot_from_status(data) if isinstance(data, dict) else None
    if snapshot is None:
        print("Claude")
        return
    write_snapshot(Path.home() / ".claude/statusline-latest.json", snapshot)
    print("Claude | 5h: {:.0f}% | 7d: {:.0f}%".format(
        snapshot["5h"]["pct"], snapshot["7d"]["pct"]))


if __name__ == "__main__":
    main()
