# -*- coding: utf-8 -*-
import os
import shutil
from pixivpy3 import *
from moviepy.editor import ImageClip
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console
from rich.progress import track
from pydub import AudioSegment
import moviepy.video.fx.all as vfx
import uuid
import cv2
import toml

config_file = 'config.toml'
CONFIG = toml.load(config_file)

api_token = CONFIG['pixiv']['api_token']
user_id = CONFIG['pixiv']['user_id']
R = CONFIG['pixiv']['avater_size']

# 创建P站的API
api = AppPixivAPI()
# API 登录
api.auth(refresh_token=api_token)

console = Console()


def check_dirs(images_dir: str, bgm_dir: str) -> None:
    """
    检测必要目录是否存在

    Args:
        images_dir (str): 图片素材目录
        bgm_dir (str): 背景音乐素材目录
    """
    if not os.path.exists(images_dir):
        console.log("请创建" + images_dir + "目录并放入你的图片文件")
    if not os.path.exists(bgm_dir):
        console.log("请创建" + bgm_dir + "目录并放入你的BGM文件")
    else:
        console.log("目录检测完毕")


# TODO 生成图片背景
def make_img_background(img_path: str, size: tuple) -> Image:
    """
    根据图片特点填充背景

    Args:
        img_path (str): 图片路径
        size (tuple): 背景大小

    Returns:
        Image: 生成的Image对象
    """
    origin_img = cv2.imread(img_path)


def resize_image(
    target_image_path: str,
    origin_target_dir: str,
    target_size: list,
) -> None:
    """
    调整图像大小

    Args:
        target_image_path (str): 存放目标路径
        origin_target_dir (str): 原始图像存放路径
        target_size (list): 调整目标大小
    """

    file_ext = target_image_path.split(".")[-1]

    exts = ["png", "jpg", "jpeg"]

    if file_ext in exts:
        image = Image.open(target_image_path)
        iw, ih = image.size  # 原始图像的尺寸
        w, h = target_size  # 目标图像的尺寸
        scale = min(w / iw, h / ih)  # 转换的最小比例

        # 保证长或宽，至少一个符合目标图像的尺寸
        nw = int(iw * scale)
        nh = int(ih * scale)

        image = image.resize((nw, nh), Image.BICUBIC)  # 缩小图像
        # image.show()
        # TODO 自动调整图片背景
        new_image = Image.new("RGB", target_size, (0, 0, 0))  # 生成黑色图像
        # 为整数除法，计算图像的位置
        new_image.paste(image,
                        ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式
        # new_image.show()

        new_image_name = uuid.uuid1().hex
        new_image_path = origin_target_dir + "/" + new_image_name + "." + file_ext

        new_image.save(new_image_path, quality=100)
    else:
        # console.log(target_image_path + "不是一个图像文件")
        pass


def mkdirs(path: str) -> bool:
    """
    创建目标路径

    Args:
        path (str): 目标路径

    Returns:
        bool: 创建结果成功为True失败为False
    """
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def rmdirs(path: str) -> bool:
    """
    删除目录及目录下的文件

    Args:
        path (str): 需要删除的路径

    Returns:
        bool: 删除结果成功为True失败为False
    """
    isExists = os.path.exists(path)
    if isExists:
        shutil.rmtree(path)
        return True
    else:
        return False


def read_dir(path: str) -> list:
    """
    读取目录下的文件

    Args:
        path (str): 路径(绝对路径)

    Returns:
        list: 文件列表(绝对路径)
    """

    # 排除干扰文件
    ignore_file = [".DS_Store", ".gitkeep"]
    paths = []
    files = os.listdir(path)
    for file in track(files, description="读取文件中..."):
        if not os.path.isdir(file):
            if file not in ignore_file:
                file_path = os.path.join(path, file)
                paths.append(file_path)
            # else:
            # console.log(file + "被排除")

    return paths


def make_bgm(
    music_path_list: list,
    output_dir: str,
    output_tmp_filename: str,
    music_total_time: int = 0,
    fade_time: list = [1000, 1000],
) -> str:
    """
    调整BGM时长以适应视频

    Args:
        music_path_list (list): BGM文件的存放路径
        output_dir (str): 转换过后BGM文件的输出路径
        output_tmp_filename (str): 转换过后的BGM文件名称
        music_total_time (int, optional): BGM的播放时长. Defaults to 0.
        fade_time (list, optional): BGM的淡入淡出时长ms. Defaults to [1000, 1000].

    Returns:
        str: 转换完成的文件存放路径
    """
    # INFO 处理多个BGM
    before_music_time = 0
    diff_time = 0
    all_music = AudioSegment.empty()
    flag = 0
    while True:
        if flag == 1:
            break
        for music_path in music_path_list:
            _music = AudioSegment.from_file(music_path)
            after_music_time = before_music_time + _music.duration_seconds * 1000

            if after_music_time >= music_total_time:
                console.log("当前添加的歌曲是：{}".format(
                    str(music_path).split("/")[-1]))
                console.log("当前的时长为： {}ms".format(before_music_time))
                diff_time = music_total_time - before_music_time
                console.log("准备截取：{}ms".format(diff_time))
                all_music = all_music + _music[len(_music) - diff_time:]
                console.log("截取完毕，现在时长为：{}ms".format(before_music_time +
                                                     diff_time))
                flag = 1
                break
            else:
                console.log("当前添加的歌曲是：{}".format(
                    str(music_path).split("/")[-1]))
                console.log("当前的时长为： {}ms".format(after_music_time))
                before_music_time = after_music_time
                all_music = all_music + _music
                # INFO 处理两个视频拼接时的细节
    bgm = all_music
    fade_in_time, fade_out_time = fade_time
    bgm.fade_in(fade_in_time).fade_out(fade_out_time)
    console.log("开始导出音频文件")
    output_file_path = os.path.join(output_dir, output_tmp_filename)
    bgm.export(output_file_path, format="mp3")
    console.log("音频暂存文件导出完毕")
    return output_file_path


def computed_time(
    img_path_list: list,
    per_img_duration: int,
    start_img_duration: int = 0,
    end_img_duration: int = 0,
) -> tuple:
    """
    根据图片数量,时长以及单个音频的长度计算出视频总时长以及音频重复次数

    Args:
        img_path_list (list): 视频包含的图片的路径列表
        per_img_duration (int): 单个图片的显示时长
        start_img_duration (int, optional): 片头长度. Defaults to 0.
        end_img_duration (int, optional): 片尾长度. Defaults to 0.

    Returns:
        tuple: 视频总时长s和音乐调整后的时长ms
    """

    console.log("开始计算最终BGM时长")
    img_count = len(img_path_list)
    video_total_time = (img_count * per_img_duration + start_img_duration +
                        end_img_duration)
    console.log("预计生成总视频长度为 {}秒".format(video_total_time))
    music_total_time = video_total_time * 1000
    console.log("BGM目标时长计算完毕,预计{}毫秒".format(music_total_time))
    return (video_total_time, music_total_time)


def make_info_img(img_size: list = [1920, 1080],
                  bg_color: list = (0, 0, 0),
                  font_color: list = (255, 255, 255),
                  des_text: str = "",
                  font_path: str = "",
                  font_size: int = 100,
                  tmp_store_path: str = "./tmp",
                  file_name: str = "output.jpg",
                  cover: bool = True,
                  cover_name: str = "cover.jpg",
                  avater: bool = False,
                  avater_url: str = "") -> str:
    """
    制作开头信息画面

    Args:
        img_size (list, optional): 图像的分辨率. Defaults to [1920, 1080].
        bg_color (tuple, optional): 背景颜色. Defaults to (0, 0, 0).
        font_color (tuple, optional): 字体颜色. Defaults to (255, 255, 255).
        des_text (str, optional): 描述信息. Defaults to "".
        font_path (str, optional): 字体文件路径. Defaults to "".
        font_size (int, optional): 字体大小. Defaults to 100.
        tmp_store_path (str, optional): 中间存储文件路径. Defaults to "./tmp".
        file_name (str, optional): 文件名. Defaults to "output.jpg".
        cover (bool,optional): 是否创建封面, Defaults to True.
        cover_name (str,optional): 封面文件保存的名称, Defaults to "cover.jpg".
        avater (bool, optional): 是否包含头像. Defaults to False.
        avater_url (str, optional): 原头像文件url. Defaults to "".

    Returns:
        str: 处理完毕的图像路径
    """

    bg = Image.new("RGB", img_size, color=bg_color)
    font = ImageFont.truetype(font_path, font_size)
    text_size = font.getsize(des_text)
    draw = ImageDraw.Draw(bg)

    # TODO 添加画师头像(圆形)
    circle_avater_path = ''
    if avater:
        prefix = str(avater_url).split('.')[-1]
        api.download(url=avater_url,
                     path=os.path.curdir + '/tmp',
                     replace=True,
                     fname='avater.' + prefix)
        avater_path = os.path.curdir + '/tmp/avater.' + prefix
        circle_avater_path = circle_clip(avater_path, prefix)
        avater_image = Image.open(circle_avater_path).convert('RGBA')
        console.log("头像制作成功")
        avater_size = avater_image.size
        # 计算字体位置
        text_coordinate = int((img_size[0] - text_size[0]) / 2), int(
            (img_size[1] + text_size[1] + int(R / 2) + 100) / 2)
        avater_coordinate = int((img_size[0] - avater_size[0]) / 2), int(
            (img_size[1] - avater_size[1] - int(R / 2)) / 2)
        console.log("头像位置处理完毕: {avater_coordinate}")
        bg.paste(avater_image, avater_coordinate, avater_image)
    else:
        # 计算字体位置
        text_coordinate = int((img_size[0] - text_size[0]) / 2), int(
            (img_size[1] - text_size[1]) / 2)
    # 写字
    draw.text(text_coordinate, des_text, font_color, font=font)
    # 要保存图片的路径
    img_path = os.path.join(tmp_store_path, file_name)
    # 保存图片
    bg.save(img_path)
    console.log("保存成功 {}".format(img_path))
    if cover:
        current_path = os.path.abspath(".")
        output_dir = CONFIG['output']['output_dir']
        output_dir = current_path + output_dir
        cover_path = os.path.join(output_dir, cover_name)
        bg.save(cover_path)
    return img_path


def make_image_clip(
    img_file_path: str,
    duration: int,
    fps: int,
    start_at: int,
    end_at: int,
    fade_time: list,
) -> ImageClip:
    """
    根据图像路径创建ImageClip

    Args:
        img_file_path (str): 图片路径
        duration (int): 显示时长
        fps (int): 帧率
        start_at (int): 轨道开始的位置
        end_at (int): 轨道结束的位置
        fade_time (list): 淡入淡出的时间s

    Returns:
        ImageClip: 转换完成的ImageClip
    """
    image_clip = (ImageClip(
        img_file_path, duration=duration *
        fps).set_fps(fps).set_start(start_at).set_end(end_at))
    image_clip = image_clip.set_pos("center")
    # 淡入淡出
    image_clip = image_clip.fx(vfx.fadein, duration=fade_time[0])
    image_clip = image_clip.fx(vfx.fadeout, duration=fade_time[1])
    return image_clip


def circle_clip(
    image_path: str,
    prefix: str,
    tmp_store_path: str = "./tmp",
) -> str:
    """
    裁剪圆形图片

    Args:
        image_path (str): 原图存放路径
        prefix (str): 图片后缀
        tmp_store_path (str, optional): 临时文件存放路径. Defaults to "./tmp".

    Returns:
        str: 返回处理完毕后的文件路径
    """
    origin_image = Image.open(image_path).convert('RGBA')
    console.log("头像读取成功")
    w, h = origin_image.size
    console.log(f"头像大小为: {w}x{h}")
    r = int(R / 2)
    if w != h:
        origin_image = origin_image.resize((R, R), Image.ANTIALIAS)
    tmp_image = Image.new('RGBA', (r * 2, r * 2), (255, 255, 255, 0))
    p_origin = origin_image.load()
    p_tmp = tmp_image.load()
    _r = float(R / 2)
    for i in track(range(R), description="裁剪头像..."):
        for j in range(R):
            x = abs(i - _r)
            y = abs(j - _r)
            __r = (pow(x, 2) + pow(y, 2))**0.5
            if __r < r:
                p_tmp[i - (_r - r), j - (_r - r)] = p_origin[i, j]
    save_path = tmp_store_path + '/' + 'circle_avater.' + prefix
    tmp_image.save(save_path)
    console.log("头像处理完毕")
    console.log(f'头像路径为({save_path})')
    return save_path


def _get_img(user_id: str, offset: int = 0) -> int:
    """
    下载当前页图片并返回下一页的偏移量

    Args:
        user_id (str): 画师ID
        offset (int, optional): 偏移量. Defaults to 0.

    Returns:
        int: 下一页的偏移量
    """
    ans = api.user_illusts(user_id=user_id, offset=offset)

    for item in track(ans.illusts, description="下载图片中..."):
        download_url = item.image_urls['large']
        api.download(url=download_url,
                     path=os.path.curdir + '/src/images',
                     replace=True)
    # INFO 获取偏移量
    offset = api.parse_qs(ans['next_url'])['offset']
    # INFO 返回偏移量,以便进行之后的执行
    return offset


def get_all_img(user_id: str = user_id):
    """
    获取画师所有的图片

    Args:
        user_id (str): 画师ID
    """
    offset = 0
    while True:
        try:
            offset = _get_img(user_id, offset)
        except TypeError:
            console.log("下载完毕")
            break


def get_user_info(user_id: str = user_id) -> dict:
    """
    获取画师信息

    Args:
        user_id (str, optional): 画师ID. Defaults to user_id.

    Returns:
        dict: 画师信息
    """
    info = api.user_detail(user_id)
    region = info.profile.region
    name = info.user.name

    console.print(info)
    console.print(f'国家: {region}')
    console.print(f'画师: {name}')
    return info