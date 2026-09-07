# Let's Build a Robot · Season 1 · LeRobot SO-101

[中文](README.md)

This repository holds every course program for Season 1 of *Let's Build a Robot*. The lessons live at the [yanshirobotics.com Learning Center](https://www.yanshirobotics.com/learn/lerobot/season-1); next to each download button, the lesson prints the file's path in this repository. If you cloned the repository, find the file at that path instead of downloading it again.

## Folders

Programs are grouped by topic, one folder per topic, not by lesson number: the same program is often used across several lessons.

| Folder | Contents | Used in |
|---|---|---|
| `Bringup/` | `so101_bus_check.py` bus communication check, `so101_calibrate.py` calibration | Lesson 6 |
| `IK/` | `so101_cartesian_demo.py` inverse-kinematics solver, `so101_visual_control.py` 3D control interface | Lesson 7 |
| `tests/` | 31 software tests against fake hardware | When you change a program |
| `tools/` | `build_control_poses.py`, kinematics data for the principle illustrations | When the illustrations are redrawn |

The lessons refer to these paths, so files are never moved or renamed; each future task gets a new folder, such as `ACT-1-Pick`. The two programs in `IK/` import each other and must stay in the same folder.

## Run commands from the repository root

Run every command from the repository root; do not `cd` into a subfolder. The relative paths in the lessons, such as `models/so101` and `calibration/follower`, then resolve the same way in every lesson.

```bash
source .venv/bin/activate
python IK/so101_cartesian_demo.py preview --model-dir models/so101 --delta-mm 0 0 2
```

Python adds a program's own folder to the module search path, so `IK/so101_visual_control.py` finds `so101_cartesian_demo.py` beside it.

## Environment

The course pins Python 3.12 and LeRobot `0.6.1`. The virtual environment (venv) is the `.venv` folder at the repository root; it keeps the course dependencies apart from the system Python. Install in the order used by Lessons 3, 7, and 8:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "lerobot[feetech]==0.6.1"
python -m pip install "viser[urdf]==1.1.0" "lerobot[kinematics,feetech]==0.6.1" \
  "cmeel-urdfdom==4.0.1" "cmeel-tinyxml2==10.0.0"
python -m pip install "lerobot[core_scripts,feetech]==0.6.1"
python -m pip check
```

The last command prints `No broken requirements found.` when the environment is complete. On Linux the default torch build includes CUDA, about 6.6 GB; training ACT (Action Chunking Transformer, the policy model covered in Lesson 13) needs it later.

The `prepare` mode from Lesson 7 downloads the arm model from TheRobotStudio's pinned revision into `models/so101`:

```bash
python IK/so101_cartesian_demo.py prepare --model-dir models/so101
```

The terminal prints `Model ready: models/so101/so101_new_calib.urdf` when the download is complete. If it prints `STOP`, fix the reported problem and run the command again.

## Tests

After changing a program in `Bringup/` or `IK/`, run the tests before committing:

```bash
python tests/test_bringup.py                            # fake hardware only
python tests/test_bringup.py --model-dir models/so101   # adds the numerical IK checks
```

The first command ends with `OK (skipped=3)`; the three skipped tests need the model. The second ends with `OK` and runs all 31. Neither opens a serial port.

`tools/build_control_poses.py` performs model-only calculations and writes the JSON used by the website's principle illustrations:

```bash
python tools/build_control_poses.py --model-dir models/so101 --output control-poses.json
```

## Three things that stay out of the repository

`.venv/` is large and tied to one machine; `calibration/` records the mid positions and ranges of your particular arm and is wrong for any other; `models/` is an upstream asset that the `prepare` command above downloads again.

## License and sources

All rights reserved for the course programs. Upstream dependencies and the model carry their own licenses: see [huggingface/lerobot](https://github.com/huggingface/lerobot) for LeRobot and [TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100) for the SO-101 model.
