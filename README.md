![LOGO](https://images.weserv.nl/?url=https://i0.hdslb.com/bfs/article/21ddb2eccb0ec77eef89708e5dbb3d14000872e7.png)

# Video Maker

---

Python 视频生成器

---

⚠️ 当前基本功能已经实现，可供优化的地方太多，正在边学，边做，进程缓慢，见谅，如果项目存在侵权行为，请立即联系删除


## 项目描述

使用 manim 进行视频的构建，只能构建一些简单的视频，复杂的部分正在研究中

### 使用方法

1. 下载 / 克隆仓库文件到本地

```shell
git clone https://github.com/MarySueTeam/Video_Maker.git
```

2. 修改配置文件内容【目前还不支持统一配置，我会不断优化的】

3. 创建本地虚拟环境

```shell
# pip install virtualvenv
virtualvenv venv
```

4. 安装 Python 的必要模块

```shell
source ./venv/bin/activate
pip install -r requirements.txt
```
5. 存放文字

```shell

文字内容存放在 ./media/words/words.txt 中
需要自己存放写入

* 其他的文字内容需要修改源代码，日后会解决，目前能力有限

```



5. 构建视频

```shell
chmod +x *.sh

./build.sh -> 主要用于最后输出
或者
./run.sh -> 主要用于日常预览
```

## TODO

-   [x] 重新设计实现步骤

## 项目结构

<!-- TODO 设计图 -->

## 致谢 🙏

- [Manim](https://github.com/ManimCommunity/manim)
- [微软 TTS](https://azure.microsoft.com/zh-cn/services/cognitive-services/text-to-speech/#overview)
- 沐瑶软笔手写体、锤子字体

## 更新日志

-   2022 年 04 月 24 日 (2.0.0):

    -   迁移到 manim 引擎 并加入暂时性的 TTS

-   2021 年 12 月 3 日:

    -   重新部署项目，使用更好更加优化的视频生成器

-   2021 年 02 月 08 日 (1.0.0):

    -   添加自动调整音频时长匹配视频
    -   支持多个 BGM
    -   添加片尾
    -   优化代码结构
