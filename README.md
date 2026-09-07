# 一起手搓机器人 · 第一季 · LeRobot SO-101

[English](README.en.md)

这个仓库放《一起手搓机器人》第一季的全部课程程序。配套教程在 [yanshirobotics.com 学习中心](https://www.yanshirobotics.com/learn/lerobot/season-1)，每课的下载按钮旁边都印着文件在这里的路径。克隆过仓库的话，按那个路径找文件，不用再下载。

## 文件夹

程序按主题分文件夹，一个主题一个文件夹，不按课次编号：同一份程序常常跨好几课。

| 文件夹 | 里面是什么 | 哪几课用 |
|---|---|---|
| `Bringup/` | `so101_bus_check.py` 通信检查、`so101_calibrate.py` 校准 | 第 6 课 |
| `IK/` | `so101_cartesian_demo.py` 逆运动学计算、`so101_visual_control.py` 三维控制界面 | 第 7 课 |
| `tests/` | 31 条软件测试，用假硬件跑 | 改程序时 |
| `tools/` | `build_control_poses.py`，生成原理图所用的运动学数据 | 重画原理图时 |

教程按这些路径引用文件，所以文件不会移动或改名；以后的任务各占一个新文件夹，例如 `ACT-1-Pick`。`IK/` 里两个程序互相调用，必须在同一个文件夹。

## 命令在仓库根目录执行

所有命令都在仓库根目录执行，不进入子文件夹。教程里 `models/so101`、`calibration/follower` 这些相对路径就都成立，每一课写法相同。

```bash
source .venv/bin/activate
python IK/so101_cartesian_demo.py preview --model-dir models/so101 --delta-mm 0 0 2
```

Python 会把程序自己所在的文件夹加进模块搜索路径，所以 `IK/so101_visual_control.py` 能找到同文件夹的 `so101_cartesian_demo.py`。

## 环境

课程锁定 Python 3.12 与 LeRobot `0.6.1`。虚拟环境（venv）是仓库根目录下的 `.venv` 文件夹，把课程依赖和系统 Python 隔开。按第 3、7、8 课的顺序安装：

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

最后一条输出 `No broken requirements found.` 就装好了。Linux 上默认安装带 CUDA 的 torch，约 6.6 GB；后面训练 ACT（Action Chunking Transformer，第 13 课讲的策略模型）要用它。

机械臂模型由第 7 课的 `prepare` 从 TheRobotStudio 的锁定版本下载到 `models/so101`：

```bash
python IK/so101_cartesian_demo.py prepare --model-dir models/so101
```

终端显示 `Model ready: models/so101/so101_new_calib.urdf` 即完成。出现 `STOP` 时先解决终端所报的问题，再执行一次。

## 测试

改过 `Bringup/` 或 `IK/` 里的程序，先跑测试再提交：

```bash
python tests/test_bringup.py                            # 只用假硬件
python tests/test_bringup.py --model-dir models/so101   # 加上数值 IK 检查
```

第一条最后一行是 `OK (skipped=3)`，跳过的 3 条需要模型；第二条是 `OK`，31 条全跑。两条都不打开串口。

`tools/build_control_poses.py` 只做模型计算，产出网站原理图所用的 JSON：

```bash
python tools/build_control_poses.py --model-dir models/so101 --output control-poses.json
```

## 不进仓库的三样

`.venv/` 太大，而且跟机器绑定；`calibration/` 记的是你这一台机械臂的中位与活动范围，换一台就不对；`models/` 是上游资产，用上面的 `prepare` 命令重新下载。

## 许可与来源

课程程序保留所有权利。上游依赖与模型各有各的许可：LeRobot 见 [huggingface/lerobot](https://github.com/huggingface/lerobot)，SO-101 模型见 [TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)。
