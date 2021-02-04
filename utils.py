# -*- coding: utf-8 -*-
import os
import shutil
from PIL import Image
from rich.console import Console
from rich.progress import track
from pydub import AudioSegment
import uuid

console = Console()


def resizeImage(target_image_path, origin_target_dir, target_size):
    """
    调整图片大小，缺失的部分用黑色填充
    :param target_image_path: 图片路径
    :param origin_target_dir: 转换完成后的暂时存目录 :type (origin_dir, target_dir)
    :param target_size: 分辨率大小 :type (width, height)
    :return:
    """

    file_ext = target_image_path.split('.')[-1]

    exts = ['png', 'jpg', 'jpeg']

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

        new_image = Image.new('RGB', target_size, (0, 0, 0, 0))  # 生成黑色图像
        # // 为整数除法，计算图像的位置
        new_image.paste(image,
                        ((w - nw) // 2, (h - nh) // 2))  # 将图像填充为中间图像，两侧为灰色的样式
        # new_image.show()

        new_image_name = uuid.uuid1().hex
        new_image_path = origin_target_dir + '/' + new_image_name + '.' + file_ext

        new_image.save(new_image_path, quality=100)
    else:
        #console.log(target_image_path + "不是一个图像文件")
        pass


def mkdirs(path):
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


def rmdirs(path):
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


def readDir(path):
    """
    读取路径下的文件并返回
    :param path: 读取的文件路径(绝对路径)
    :return: 文件绝对路径的列表
    """
    paths = []
    files = os.listdir(path)
    for file in track(files, description="读取图片文件中..."):
        if not os.path.isdir(file):
            file_path = os.path.join(path, file)
            #console.log(file_path)
            paths.append(file_path)
    return paths


def makeBGM(input_dir,
            output_dir,
            output_tmp_filename,
            times=1,
            fade_time=1000):
    """
    根据需要转换BGM
    :param input_dir: BGM文件存储路径
    :param output_dir: 转换过后BGM文件输出路径，中转文件的暂时存放路径
    :param output_tmp_filename: 转换过后BGM文件名称
    :param times: BGM文件循环播放的次数
    :param fade_time: BGM淡入淡出时长ms
    :return: 转换完成的文件路径
    """
    bgm = ""
    bgm_file_paths = readDir(input_dir)
    for bgm_file_path in bgm_file_paths:
        bgm = AudioSegment.from_mp3(bgm_file_path)
        break
    console.log(bgm.duration_seconds, bgm.dBFS, bgm.frame_rate)
    bgm *= times
    bgm.fade_in(fade_time).fade_out(fade_time)
    console.log("开始导出音频文件")
    output_file_path = os.path.join(output_dir, output_tmp_filename)
    bgm.export(output_file_path, format='mp3')
    console.log("音频暂存文件导出完毕")
    return output_file_path
