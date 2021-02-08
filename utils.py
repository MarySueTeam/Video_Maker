# -*- coding: utf-8 -*-
import os
import shutil
from moviepy.editor import ImageClip
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console
from rich.progress import track
from pydub import AudioSegment
import moviepy.video.fx.all as vfx
import uuid

console = Console()


def check_dirs(images_dir: str, bgm_dir: str) -> None:
    """
    检测本应该存在的目录是否存在
    :param images_dir: 图片文件目录
    :param bgm_dir: BGM问价目录
    """
    if not os.path.exists(images_dir):
        console.log("请创建" + images_dir + "目录并放入你的图片文件")
    if not os.path.exists(bgm_dir):
        console.log("请创建" + bgm_dir + "目录并放入你的BGM文件")
    else:
        console.log("目录检测完毕")


def resize_image(
    target_image_path: str,
    origin_target_dir: str,
    target_size: tuple,
    bg_color: tuple,
) -> None:
    """
    调整图片大小，缺失的部分用黑色填充

    :param target_image_path: 图片路径
    :param origin_target_dir: 转换完成后的暂时存目录 :type (origin_dir, target_dir)
    :param target_size: 分辨率大小 :type (width, height)
    :param bg_color: 扩展部分颜色 :type (R,G,B)
    :return:
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

        new_image = Image.new("RGB", target_size, bg_color)  # 生成黑色图像
        # 为整数除法，计算图像的位置
        new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式
        # new_image.show()

        new_image_name = uuid.uuid1().hex
        new_image_path = origin_target_dir + "/" + new_image_name + "." + file_ext

        new_image.save(new_image_path, quality=100)
    else:
        # console.log(target_image_path + "不是一个图像文件")
        pass


def mkdirs(path: str) -> bool:
    """
    创建目录

    :param path: 需要创建的路径
    :return: 存在并成功返回True，不存在返回False
    """
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return True
    else:
        return False


def rmdirs(path: str) -> bool:
    """
    删除目录及目录下面的文件

    :param path: 需要删除的目录
    :return: 存在并删除成功返回True，不存在返回False
    """
    isExists = os.path.exists(path)
    if isExists:
        shutil.rmtree(path)
        return True
    else:
        return False


def read_dir(path: str) -> list:
    """
    读取路径下的文件并返回

    :param path: 读取的文件路径(绝对路径)
    :return: 文件绝对路径的列表
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
    fade_time: tuple = (1000, 1000),
) -> str:
    """
    调整BGM时长以适应视频

    :param music_path_list: BGM文件存储路径
    :param output_dir: 转换过后BGM文件输出路径，中转文件的暂时存放路径
    :param output_tmp_filename: 转换过后BGM文件名称
    :param music_total_time: BGM的播放时长,
    :param fade_time: BGM淡入淡出时长ms,(淡入时长,淡出时长)
    :return: 转换完成的文件路径和BGM时长(path,time)
    """
    # TODO 处理多个BGM
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
                console.log("当前添加的歌曲是：{}".format(str(music_path).split("/")[-1]))
                console.log("当前的时长为： {}ms".format(before_music_time))
                diff_time = music_total_time - before_music_time
                console.log("准备截取：{}ms".format(diff_time))
                all_music = all_music + _music[len(_music) - diff_time :]
                console.log("截取完毕，现在时长为：{}ms".format(before_music_time + diff_time))
                flag = 1
                break
            else:
                console.log("当前添加的歌曲是：{}".format(str(music_path).split("/")[-1]))
                console.log("当前的时长为： {}ms".format(after_music_time))
                before_music_time = after_music_time
                all_music = all_music + _music
                # TODO 处理两个视频拼接时的细节
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
    根据图片数量、图片时长、以及单个音频长度计算出视频总时长以及音频的重复次数

    :param img_list: 视频所包含的图片路径列表
    :param per_img_duration: 单个图片的显示时长
    :param start_img_duration: 片头长度
    :param end_img_duration: 片尾长度
    :return 返回总的视频时长（单位：秒）以及音乐调整后的时长（单位：毫秒）
    """

    console.log("开始计算最终BGM时长")
    img_count = len(img_path_list)
    video_total_time = (
        img_count * per_img_duration + start_img_duration + end_img_duration
    )
    console.log("预计生成总视频长度为 {}秒".format(video_total_time))
    music_total_time = video_total_time * 1000
    console.log("BGM目标时长计算完毕,预计{}毫秒".format(music_total_time))
    return (video_total_time, music_total_time)


def make_info_img(
    img_size: tuple = (1920, 1080),
    bg_color: tuple = (255, 255, 255),
    font_color: tuple = (255, 255, 255),
    des_text: str = "",
    font_path: str = "./fonts/Smartisan_Compact-Regular.ttf",
    font_size: int = 100,
    tmp_store_path: str = "./tmp",
    file_name: str = "output.jpg",
) -> str:
    """
    创建视频开头图像

    :param img_size: 图片大小，通常为视频分辨率
    :param des_text: 显示文字内容
    :param font_path: 字体文件路径
    :param font_size: 字体大小
    :return: 生成的图片所存放的路径
    """
    bg = Image.new("RGB", img_size, color=bg_color)
    font = ImageFont.truetype(font_path, font_size)
    text_width = font.getsize(des_text)
    draw = ImageDraw.Draw(bg)
    # 计算字体位置
    text_coordinate = int((img_size[0] - text_width[0]) / 2), int(
        (img_size[1] - text_width[1]) / 2
    )
    # 写字
    draw.text(text_coordinate, des_text, font_color, font=font)
    # 要保存图片的路径
    img_path = os.path.join(tmp_store_path, file_name)
    # 保存图片
    bg.save(img_path)
    console.log("保存成功 {}".format(img_path))
    return img_path


def make_image_clip(
    img_file_path: str,
    duration: int,
    fps: int,
    start_at: int,
    end_at: int,
    fade_time: tuple,
) -> ImageClip:
    """
    根据图像路径创建ImageClip
    :param img_file_path: 图片的路径
    :param duration: 显示时长
    :param fps: 帧率
    :param start_at: 轨道开始位置
    :param end_at: 轨道结束位置
    :param fade_time: 淡入淡出时间,单位秒
    :return: ImageClip类型
    """
    image_clip = (
        ImageClip(img_file_path, duration=duration * fps)
        .set_fps(fps)
        .set_start(start_at)
        .set_end(end_at)
    )
    image_clip = image_clip.set_pos("center")
    # 淡入淡出
    image_clip = image_clip.fx(vfx.fadein, duration=fade_time[0])
    image_clip = image_clip.fx(vfx.fadeout, duration=fade_time[1])
    return image_clip