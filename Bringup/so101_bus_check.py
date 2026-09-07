#!/usr/bin/env python3
"""Read a single SO-101 bus through LeRobot 0.6.1; never write motor registers.

Read-only software does not guarantee an unpowered or motionless arm. The
operator must complete the pre-power inspection and be able to cut motor power.
"""
from __future__ import annotations

import argparse
import math
import sys
import time
from importlib.metadata import version

JOINT_NAMES = ("shoulder_pan", "shoulder_lift", "elbow_flex", "wrist_flex", "wrist_roll", "gripper")
LEROBOT_VERSION = "0.6.1"
# Ten short reads detect interruptions during this check, not long-term reliability.
DEFAULT_SAMPLES = 10
DEFAULT_INTERVAL_SECONDS = 0.2


def check_bus(bus, *, role, samples, interval, output=print, sleep=time.sleep):
    prefix = "F" if role == "follower" else "L"
    try:
        # The handshake reads the expected IDs, model numbers and firmware.
        bus.connect()
        for name in JOINT_NAMES:
            if bus.read("Torque_Enable", name, normalize=False) != 0:
                raise RuntimeError("Torque is already enabled. Cut motor power and investigate before continuing.")
        output("PORT " + str(bus.port))
        output("ID " + " ".join(f"{prefix}{i}={i}" for i in range(1, len(JOINT_NAMES) + 1)))
        for sample in range(samples):
            positions = bus.sync_read("Present_Position", normalize=False)
            if set(positions) != set(JOINT_NAMES) or not all(math.isfinite(float(v)) for v in positions.values()):
                raise RuntimeError("Incomplete or invalid position response; do not continue to calibration.")
            output(f"READ {sample + 1}/{samples} " + " ".join(f"{name}={positions[name]}" for name in JOINT_NAMES))
            if sample + 1 < samples:
                sleep(interval)
        output("PASS: six expected motors answered every read. Role label is operator-assigned; motion is not tested.")
    finally:
        # Even a failed handshake can leave the serial port open. The default
        # disconnect would write Torque_Enable, so explicitly disable that write.
        if bus.is_connected:
            bus.disconnect(disable_torque=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", required=True, help="Actual port identified with USB power only")
    parser.add_argument("--role", required=True, choices=("leader", "follower"))
    parser.add_argument("--samples", type=int, default=DEFAULT_SAMPLES)
    parser.add_argument("--interval", type=float, default=DEFAULT_INTERVAL_SECONDS)
    args = parser.parse_args(argv)
    if args.samples < 1 or not math.isfinite(args.interval) or args.interval < 0:
        parser.error("samples must be positive and interval finite and non-negative")
    try:
        if version("lerobot") != LEROBOT_VERSION:
            raise RuntimeError(f"Use lerobot=={LEROBOT_VERSION} in the course environment.")
        from lerobot.motors import Motor, MotorNormMode
        from lerobot.motors.feetech import FeetechMotorsBus
        bus = FeetechMotorsBus(port=args.port, motors={
            name: Motor(index, "sts3215", MotorNormMode.DEGREES)
            for index, name in enumerate(JOINT_NAMES, 1)
        })
        check_bus(bus, role=args.role, samples=args.samples, interval=args.interval)
        return 0
    except KeyboardInterrupt:
        print("Interrupted. Motor power has not been switched off by this program.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"STOP: {exc}\nCut motor power before touching wiring. This program does not switch off motor power.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
