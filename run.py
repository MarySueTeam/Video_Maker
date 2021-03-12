# -*- coding: utf-8 -*-
import os
from rich.console import Console
from moviepy.editor import CompositeVideoClip, AudioFileClip
from utils import (
    check_dirs,
    make_bgm,
    resize_image,
    mkdirs,
    rmdirs,
    read_dir,
    computed_time,
    make_info_img,
    make_image_clip,
)
from rich.progress import track

from pixivpy3 import *

api = AppPixivAPI()
console = Console()

images_dir = "/src/images"
bgm_dir = "/src/music"
tmp_dir = "/tmp"
tmp_image_dir = "/tmp/images"
tmp_music_dir = "/tmp/music"
output_dir = "/dist/"
output_filename = "out.mp4"
display_size = (1920, 1080)
fps = 30
api_token = 'ADpdU_RmJzHQ1-o_5o5ZXAhNx3HVAZqPhjgd-ZN2o8E'

start_img_duration = 10  # 片头图片显示时长
per_img_display_time = 10  # 每张图片显示的时长
end_img_duration = 10  # 片尾图片显示时长

start_img_fade_time = (0.5, 0.5)  # 第一张图片的淡入淡出时间
per_img_fade_time = (0.5, 0.5)  # 中间每张图片的淡入淡出时间
end_img_fade_time = (0.5, 0.5)  # 结尾图片的淡入淡出时间
bgm_fade_time = (1, 1)  # 背景音乐的淡入淡出时间

# 片头片尾
# TODO 自动设置替代
des_text = "画师：Aoi Ogata"
end_text = "谢谢观看"
# 字体路径
font_path = "./fonts/Smartisan_Compact-Regular.ttf"
# 背景颜色
# TODO 使用自动设置替代
bg_color = (0, 0, 0)
# 字体颜色
# TODO 使用自动设置替代
font_color = (255 - bg_color[0], 255 - bg_color[1], 255 - bg_color[2])

current_path = os.path.abspath(".")
images_dir = current_path + images_dir
bgm_dir = current_path + bgm_dir
tmp_dir = current_path + tmp_dir
tmp_music_dir = current_path + tmp_music_dir
tmp_image_dir = current_path + tmp_image_dir
output_dir = current_path + output_dir
output_file = output_dir + output_filename
bgm_fade_time = (bgm_fade_time[0] * 1000, bgm_fade_time[1] * 1000)

api.auth(refresh_token=api_token)


def main():
    """程序的主函数
    程序运行的主要逻辑
    """
    check_dirs(images_dir, bgm_dir)
    if mkdirs(tmp_dir):
        console.log(tmp_dir + "创建成功")
    if mkdirs(tmp_image_dir):
        console.log(tmp_image_dir + "创建成功")
    if mkdirs(tmp_music_dir):
        console.log(tmp_music_dir + "创建成功")
    if mkdirs(output_dir):
        console.log(output_dir + "创建成功")
    img_paths = read_dir(images_dir)
    for img_file in track(img_paths, description="调整图片中..."):
        resize_image(img_file, tmp_image_dir, display_size)

    img_paths = read_dir(tmp_image_dir)
    bgm_paths = read_dir(bgm_dir)

    # 计算时长
    video_total_time, music_total_time = computed_time(img_paths,
                                                       per_img_display_time,
                                                       start_img_duration,
                                                       end_img_duration)

    clips = []

    # 创建片头介绍文字
    console.log("开始创建开头文字")

    video_start_info_img_path = make_info_img(
        display_size,
        bg_color,
        font_color,
        des_text,
        font_path,
        100,
        tmp_image_dir,
        "start_info.jpg",
    )
    video_start_info_img_clip = make_image_clip(
        video_start_info_img_path,
        start_img_duration,
        fps,
        0,
        start_img_duration,
        start_img_fade_time,
    )
    clips.append(video_start_info_img_clip)
    console.log("开头文字创建完毕")

    count = 0
    for img_path in track(img_paths, description="添加图片帧..."):

        tmp_space_start = per_img_display_time * count + start_img_duration
        tmp_space_end = per_img_display_time * (count + 1) + start_img_duration
        img_clip = make_image_clip(
            img_path,
            per_img_display_time,
            fps,
            tmp_space_start,
            tmp_space_end,
            per_img_fade_time,
        )
        clips.append(img_clip)
        count = count + 1

    # 创建片尾文字
    console.log("开始创建片尾文字")

    video_end_info_img_path = make_info_img(
        display_size,
        bg_color,
        font_color,
        end_text,
        font_path,
        100,
        tmp_image_dir,
        "end_info.jpg",
    )
    video_end_info_img_clip = make_image_clip(
        video_end_info_img_path,
        start_img_duration,
        fps,
        video_total_time - end_img_duration,
        video_total_time,
        end_img_fade_time,
    )
    clips.append(video_end_info_img_clip)
    console.log("片尾文字创建完毕")

    bgm_tmp_file_path = make_bgm(bgm_paths, tmp_music_dir, "bgm.mp3",
                                 music_total_time, bgm_fade_time)
    console.log("经过处理的音频文件路径为" + bgm_tmp_file_path)
    bgm_clip = AudioFileClip(bgm_tmp_file_path)
    console.log("背景音乐切片处理完毕")

    # 混合CLIP
    console.log("开始将帧切片合并为视频文件")
    final_clip = CompositeVideoClip(clips)
    console.log("开始合并背景音乐切片")
    final_clip = final_clip.set_audio(bgm_clip)
    console.log("开始导出视频文件到" + output_file)
    final_clip.write_videofile(output_file)
    # 清除中间转存文件
    console.log("清除中间转换缓存文件")
    rmdirs(tmp_dir)
    console.log("中间转换缓存文件清理完毕")


if __name__ == "__main__":
    console.log("程序开始运行")
    main()
