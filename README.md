![LOGO](https://images.weserv.nl/?url=https://i0.hdslb.com/bfs/article/21ddb2eccb0ec77eef89708e5dbb3d14000872e7.png)

# Video Maker

![syntax check](https://github.com/allinu/Video_Maker/workflows/syntax%20check/badge.svg)

⚠️ 当前基本功能已经实现，可供优化的地方太多，正在边学，便做，进程缓慢，见谅

Python 视频生成器(支持一键生成P站搬运视频)

## 项目描述

Python，以及 `moviepy` 根据图片创作出视频，使用 `rich` 优化控制台输出样式，代码执行不会破坏素材源文件

## 目录介绍

目录主要分为 `必要目录` 和 `自动生成目录`，必要目录随项目下载就存在，不能删除，并且里面需要放置生成视频所需要的图片素材文件，图片素材文件格式可以为 `jpg`,`png`,`jpeg`，暂不支持其他格式

### 必要目录

> 必须存在的目录,并且按照规定放置素材文件

- `src/images`: 存放原始图片
- `src/music`: 存放 BGM

### 自动生成目录

> 如果存在将跳过,没有将自动创建

- `tmp/`: 程序执行过程中中间文件的存储路径（运行完毕自动清理）
- `dist/`: 输出视频存放目录

### 使用方法

1. 下载 / 克隆仓库文件到本地

```shell
git clone https://github.com/allinu/Video_Maker.git
```

2. 将图片及 BGM 拷贝至指定目录

3. 创建本地虚拟环境

```shell
virtualvenv venv
```
4. 安装 Python 的必要模块

```shell
source ./venv/bin/activate
pip install -r requirements.txt
```
5. 执行 `run.py` 文件

```shell
python run.py
```

## TODO

- [X] 自动生成视频
- [X] 自动获取P站图片
- [ ] 智能填充背景(根据不同的图片类型填充背景)
- [X] 支持 BGM 添加
    - [X] 自动调整视频与音频的长度
- [X] 支持片头添加介绍文字
    - [ ] 支持显示头像
    - [ ] 支持复杂点的配文
- [ ] 支持自动发布视频到 Bilibili
    - [ ] 支持观众交互式编辑
- [X] 支持配置文件


## 项目结构

![](https://images.weserv.nl/?url=https://i0.hdslb.com/bfs/article/b80e5315efbf70d58454c35d1b8d67fbca559f1c.png)

## 更新日志

- 2021 年 02 月 08 日 (1.0.0):
    - 添加自动调整音频时长匹配视频
    - 支持多个 BGM
    - 添加片尾
    - 优化代码结构
