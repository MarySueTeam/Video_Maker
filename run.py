# -*- coding: utf-8 -*-
import os
from rich.console import Console
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, ImageClip
from utils import makeBGM, resizeImage, mkdirs, rmdirs, readDir
import moviepy.video.fx.all as vfx
from rich.progress import track

console = Console()

images_dir = '/src/images'
bgm_dir = '/src/music'
tmp_dir = '/tmp'
tmp_image_dir = '/tmp/images'
tmp_music_dir = '/tmp/music'
output_dir = '/dist/'
output_filename = 'out.mp4'
fps = 30

current_path = os.path.abspath('.')
images_dir = current_path + images_dir
bgm_dir = current_path + bgm_dir
tmp_dir = current_path + tmp_dir
tmp_music_dir = current_path + tmp_music_dir
tmp_image_dir = current_path + tmp_image_dir
output_dir = current_path + output_dir
output_file = output_dir + output_filename
from pydub import AudioSegment


def check_dirs():
    if not os.path.exists(images_dir):
        console.log("请创建" + images_dir + "目录并放入你的图片文件")
    if not os.path.exists(bgm_dir):
        console.log("请创建" + bgm_dir + "目录并放入你的BGM文件")
    else:
        console.log("目录检测完毕")


def main():
    check_dirs()
    if mkdirs(tmp_dir):
        console.log(tmp_dir + "创建成功")
    if mkdirs(tmp_image_dir):
        console.log(tmp_image_dir + "创建成功")
    if mkdirs(tmp_music_dir):
        console.log(tmp_music_dir + "创建成功")
    if mkdirs(output_dir):
        console.log(output_dir + "创建成功")
    img_paths = readDir(images_dir)
    for img_file in track(img_paths, description="调整图片中..."):
        resizeImage(img_file, tmp_image_dir, (1920, 1080))

    img_paths = readDir(tmp_image_dir)

    # clip = ImageSequenceClip(img_paths, fps=0.2).fx(vfx.fadein, duration=0.5)
    # clip.write_videofile(output_file)

    clips = []
    count = 0
    for img_path in track(img_paths, description="添加图片帧..."):
        tmp_space_start = 10 * count
        tmp_space_end = 10 * (count + 1)
        img_clip = (ImageClip(img_path, duration=10 * fps)).set_fps(
            fps).set_start(tmp_space_start).set_end(tmp_space_end)
        img_clip = img_clip.set_pos('center')
        # 淡入淡出
        img_clip = img_clip.fx(vfx.fadein, duration=0.5)
        img_clip = img_clip.fx(vfx.fadeout, duration=0.5)
        clips.append(img_clip)
        count = count + 1

    bgm_tmp_file_path = makeBGM(input_dir=bgm_dir,
                                output_dir=tmp_music_dir,
                                output_tmp_filename="bgm.mp3",
                                times=3,
                                fade_time=1000)
    console.log(bgm_tmp_file_path)
    bgm_clip = AudioFileClip(bgm_tmp_file_path)

    # 混合CLIP
    console.log("开始将帧合并为视频文件")
    final_clip = CompositeVideoClip(clips)
    console.log("开始添加背景音乐文件")
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
