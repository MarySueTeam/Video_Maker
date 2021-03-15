# -*- coding: utf-8 -*-
import os
import toml
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
    get_user_info,
    get_all_img,
)
from rich.progress import track

console = Console()

config_file = 'config.toml'
CONFIG = toml.load(config_file)


def main():
    """程序的主函数
    程序运行的主要逻辑
    """
    images_dir = CONFIG['source']['images_dir']
    bgm_dir = CONFIG['source']['bgm_dir']
    tmp_dir = CONFIG['tmp']['tmp_dir']
    tmp_image_dir = CONFIG['tmp']['tmp_image_dir']
    tmp_music_dir = CONFIG['tmp']['tmp_music_dir']
    output_dir = CONFIG['output']['output_dir']
    output_filename = CONFIG['output']['output_filename']
    display_size = CONFIG['video']['display_size']
    fps = CONFIG['video']['fps']

    start_img_duration = CONFIG['image']['start_img_duration']
    per_img_display_time = CONFIG['image']['per_img_display_time']
    end_img_duration = CONFIG['image']['end_img_duration']

    start_img_fade_time = CONFIG['fade_time']['start_img_fade_time']
    per_img_fade_time = CONFIG['fade_time']['per_img_fade_time']
    end_img_fade_time = CONFIG['fade_time']['end_img_fade_time']
    bgm_fade_time = CONFIG['fade_time']['bgm_fade_time']

    if_pixiv = CONFIG['pixiv']['pixiv']

    # 片头片尾
    # TODO 自动设置替代
    des_text = CONFIG['text']['des_text']
    end_text = CONFIG['text']['end_text']
    # 字体路径
    font_path = CONFIG['font']['font_path']
    font_size = CONFIG['font']['font_size']
    # 背景颜色
    # TODO 使用自动设置替代
    bg_color = CONFIG['color']['bg_color']
    bg_color = tuple(bg_color)
    # 字体颜色
    # TODO 使用自动设置替代
    font_color = CONFIG['color']['font_color']
    font_color = tuple(font_color)

    current_path = os.path.abspath(".")
    images_dir = current_path + images_dir
    bgm_dir = current_path + bgm_dir
    tmp_dir = current_path + tmp_dir
    tmp_music_dir = current_path + tmp_music_dir
    tmp_image_dir = current_path + tmp_image_dir
    output_dir = current_path + output_dir
    output_file = output_dir + output_filename
    bgm_fade_time = (bgm_fade_time[0] * 1000, bgm_fade_time[1] * 1000)
    check_dirs(images_dir, bgm_dir)
    if mkdirs(tmp_dir):
        console.log(tmp_dir + "创建成功")
    if mkdirs(tmp_image_dir):
        console.log(tmp_image_dir + "创建成功")
    if mkdirs(tmp_music_dir):
        console.log(tmp_music_dir + "创建成功")
    if mkdirs(output_dir):
        console.log(output_dir + "创建成功")

    avater_url = ""
    if des_text == "":
        info = get_user_info()
        region = info.profile.region
        name = info.user.name
        avater_url = info.user.profile_image_urls.medium
        des_text = name

    # INFO 获取P站图片

    if if_pixiv:
        get_all_img()

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

    # INFO 创建片头介绍文字
    console.log("开始创建开头文字")
    video_start_info_img_path = make_info_img(img_size=display_size,
                                              bg_color=bg_color,
                                              font_color=font_color,
                                              des_text=des_text,
                                              font_path=font_path,
                                              font_size=font_size,
                                              tmp_store_path=tmp_dir,
                                              file_name="start_info.jpg",
                                              avater=True,
                                              avater_url=avater_url)
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

    video_end_info_img_path = make_info_img(img_size=display_size,
                                            bg_color=bg_color,
                                            font_color=font_color,
                                            des_text=end_text,
                                            font_path=font_path,
                                            font_size=font_size,
                                            tmp_store_path=tmp_dir,
                                            file_name="end_info.jpg",
                                            cover=False)
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
