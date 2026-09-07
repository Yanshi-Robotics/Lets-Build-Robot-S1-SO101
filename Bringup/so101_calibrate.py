#!/usr/bin/env python3
"""Run the official LeRobot 0.6.1 calibration with torque disabled throughout.

The course entry point intentionally skips Robot.connect()/configure(): the
Follower's generic configure enables torque before the official CLI calibrates.
This program still writes motor registers. Only the hardware operator may run it.
"""
import argparse
import sys
from importlib.metadata import version
from pathlib import Path

LEROBOT_VERSION = "0.6.1"


def calibrate_device(device):
    try:
        # Read-only bus handshake; do not call the torque-enabling robot connect.
        device.bus.connect()
        device.bus.disable_torque()
        # Preserve the official preparation of Phase/position representation,
        # without using the robot configure method that reenables torque.
        device.bus.configure_motors()
        device.calibrate()
    finally:
        if device.bus.is_connected:
            try:
                device.bus.disable_torque()
            finally:
                device.bus.disconnect(disable_torque=False)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--role", choices=("follower", "leader"), required=True)
    parser.add_argument("--port", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--calibration-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if version("lerobot") != LEROBOT_VERSION:
            raise RuntimeError(f"Use lerobot=={LEROBOT_VERSION}")
        options = dict(port=args.port, id=args.id, calibration_dir=args.calibration_dir, use_degrees=True)
        if args.role == "follower":
            from lerobot.robots.so_follower import SO101Follower, SO101FollowerConfig
            device = SO101Follower(SO101FollowerConfig(**options))
        else:
            from lerobot.teleoperators.so_leader import SO101Leader, SO101LeaderConfig
            device = SO101Leader(SO101LeaderConfig(**options))
        print("Support the arm: this program disables torque and writes calibration. Keep fingers clear of pinch points.")
        if input("Type CALIBRATE to continue: ").strip() != "CALIBRATE":
            return 0
        calibrate_device(device)
        print(f"Calibration file: {device.calibration_fpath}. Disconnect DC power before changing wiring.")
        return 0
    except KeyboardInterrupt:
        print("Interrupted. Cut motor power before investigating; software is not a physical cutoff.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"STOP: {exc}\nCut motor power before investigating. Torque release can fail if communication is lost.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
