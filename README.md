# 一起手搓机器人 · Season 1 · LeRobot SO-101

《一起手搓机器人》第一季的课程代码。配套教程在
[yanshirobotics.com 的学习中心](https://www.yanshirobotics.com/learn/lerobot/season-1)。

## 目录怎么分

一个仓，一个 Python 环境，按主题分文件夹。

```
lerobot-so101/
├── .venv/            共用环境，不进仓
├── Bringup/          通信检查与校准
├── IK/               逆运动学与三维控制界面
├── calibration/      校准结果，不进仓
└── models/           SO-101 模型，不进仓
```

文件夹按主题命名，**不标课程号**。同一份代码常常跨好几课，标了号反而对不上。
后面加新内容照这个格式：模型或方法在前，任务在后，例如 `ACT-1-Pick`、`Pi0-1-Pick`。

**已经放出去的路径不再改动**。教程每个下载按钮旁边都印着文件在这里的路径，
克隆过仓库的同学按那个路径找文件。要加新内容就新建文件夹，不要移动或改名现有的。

## 怎么跑

**命令一律在仓根执行**，不要 `cd` 进子文件夹。这样 `models/so101`、`calibration/follower`
这些相对路径在所有课里都是同一个写法：

```bash
source .venv/bin/activate
python IK/so101_cartesian_demo.py preview --model-dir models/so101 --delta-mm 0 0 2
```

## 环境

Python 3.12 + LeRobot 0.6.1。按第 3、7、8 课的命令依次安装：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "lerobot[feetech]==0.6.1"
python -m pip install "viser[urdf]==1.1.0" "lerobot[kinematics,feetech]==0.6.1" \
  "cmeel-urdfdom==4.0.1" "cmeel-tinyxml2==10.0.0"
python -m pip install "lerobot[core_scripts,feetech]==0.6.1"
```

Linux 上默认装的是 CUDA 版 torch，约 6.6 GB；后面训练 ACT 要用它。

`models/` 由第 7 课的 `prepare` 从 TheRobotStudio 的锁定版本下载，随时可以重取：

```bash
python IK/so101_cartesian_demo.py prepare --model-dir models/so101
```

## 测试与工具

```bash
python tests/test_bringup.py                            # 31 条软件测试，接假机械臂，不碰硬件
python tests/test_bringup.py --model-dir models/so101   # 加上数值 IK 检查，需要上面装好的环境
python tools/build_control_poses.py --model-dir models/so101 --output control-poses.json
```

`tests/` 只用假硬件，`tools/` 只做模型计算，两者都不打开串口。
改过 `Bringup/` 或 `IK/` 里的程序，先跑一遍测试再提交。

能跑的东西只在这个仓里。课程网站上的同名文件只用来下载，不在网站里执行。

## 三样东西不进仓

`.venv/` 体积太大且跟机器绑定；`calibration/` 记的是你这一台实物的中位与活动范围，
换一台就不对；`models/` 是上游资产，用上面那条命令重新下载即可。

## 许可

课程代码，保留所有权利。上游依赖与模型各自遵循自己的许可：
LeRobot 见 [huggingface/lerobot](https://github.com/huggingface/lerobot)，
SO-101 模型见 [TheRobotStudio/SO-ARM100](https://github.com/TheRobotStudio/SO-ARM100)。
