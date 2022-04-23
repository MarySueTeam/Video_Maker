from manim import *
from TTS.TTS import get_mp3_file
from utils import cut, get_duration, deal_text
import time


class Video(Scene):
    def construct(self):
        # INFO 视频开头
        LOGO = ImageMobject("./media/images/logo.png").scale(0.3).to_edge(UP, buff=2)
        Slogan_text = "为你收集日落时的云朵，为你收藏下雨后的天空"
        get_mp3_file(text=f"{Slogan_text}", output_path="./media/sounds/video_start", rate="-10%")
        Slogan = Text(Slogan_text, font="Muyao-Softbrush", weight=MEDIUM, color="#FCA113").scale(0.7).next_to(LOGO, DOWN, buff=1)
        self.play(FadeIn(LOGO, run_time=0.1))
        self.wait(0.5)
        self.play(FadeIn(Slogan), run_time=1)
        self.add_sound("./media/sounds/video_start.mp3")
        self.wait(5)
        self.play(FadeOut(Slogan, LOGO))

        # INFO 主视频内容
        LOGO = ImageMobject("./media/images/logo.png").scale(0.1).to_edge(UL)
        username = Text("@仙女玛丽苏吖",font="Muyao-Softbrush").scale(0.5).next_to(LOGO, RIGHT)
        self.add(LOGO, username)
        title = "在本子上写上他的名字"
        title = "《" + title + "》"
        title = Text(title, font="Muyao-Softbrush", color=ORANGE).scale(0.5).to_edge(UP, buff=0.75)
        self.add(title)
        with open("./media/words/words.txt", "rt", encoding="utf-8") as f:
            content = f.readline()
            while content:
                audio_path = "./media/sounds/video_content_"+str(round(time.time()*1000))
                # content = deal_text(content)
                get_mp3_file(text=content,output_path=audio_path,rate="-10%")
                audio_path = audio_path + ".mp3"
                audio_time = get_duration(audio_path)
                content = MarkupText(content, font="Muyao-Softbrush", font_size=60, justify=True).scale(0.5)
                run_time = len(content)//50
                self.play(Write(content), run_time=run_time)
                self.add_sound(audio_path, time_offset = 1)
                self.wait(audio_time)
                self.play(FadeOut(content))
                content = f.readline()
        self.play(FadeOut(title,username,LOGO))

        # INFO 视频结尾
        LOGO = ImageMobject("./media/images/logo.png").scale(0.2).to_edge(UP, buff=2)

        messages_text = "你可以在下面的平台找到我，这一期就先到这里，我们下期再见。拜拜～"
        messages = Text("-你可以在下面的平台找到我-", font="Muyao-Softbrush").scale(0.4).next_to(LOGO, DOWN)

        # INFO 获取音频文件 
        get_mp3_file(text=f"{messages_text}",output_path="./media/sounds/video_end",rate="-10%")

        gonzhonghao = ImageMobject("./media/images/icon/weixin.png").scale(0.2)
        username1 = Text("@仙女玛丽苏", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(gonzhonghao)
        zhihu = ImageMobject("./media/images/icon/zhihu.png").next_to(gonzhonghao, RIGHT, buff=1).scale(0.2)
        username2 = Text("@仙女玛丽苏", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(zhihu)
        xiaohongshu = ImageMobject("./media/images/icon/xiaohongshu.png").next_to(zhihu, RIGHT, buff=1).scale(0.2)
        username3 = Text("@仙女玛丽苏", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(xiaohongshu)

        bilibili = ImageMobject("./media/images/icon/bilibili.png").next_to(gonzhonghao).scale(0.2)
        username4 = Text("@仙女玛丽苏吖", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(bilibili)
        douyin = ImageMobject("./media/images/icon/douyin.png").next_to(bilibili, RIGHT, buff=1).scale(0.2)
        username5 = Text("@仙女玛丽苏", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(douyin)
        toutiao = ImageMobject("./media/images/icon/toutiao1.png").next_to(douyin, RIGHT, buff=1).scale(0.2)
        username6 =Text("@仙女玛丽苏", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(toutiao)

        jianshu = ImageMobject("./media/images/icon/jianshu.png").next_to(bilibili).scale(0.2)
        username7 = Text("@仙女玛丽苏", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(jianshu)
        kuaishou = ImageMobject("./media/images/icon/kuaishou.png").next_to(jianshu, RIGHT, buff=1).scale(0.2)
        username8 = Text("@仙女玛丽苏吖", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(kuaishou)
        xiguashipin = ImageMobject("./media/images/icon/xiguashipin.png").next_to(kuaishou, RIGHT, buff=1).scale(0.2)
        username9 = Text("@仙女玛丽苏", font="Smartisan Compact CNS", weight=MEDIUM).scale(0.25).next_to(xiguashipin)

        Recommend_group1 = Group(
            gonzhonghao,
            username1,
            zhihu,
            username2,
            xiaohongshu,
            username3,
        ).next_to(LOGO, DOWN, buff=1)
        Recommend_group2 = Group(
            bilibili,
            username4,
            douyin,
            username5,
            toutiao,
            username6,
        ).next_to(Recommend_group1, DOWN, buff=0.2)
        Recommend_group3 = Group(
            jianshu,
            username7,
            kuaishou,
            username8,
            xiguashipin,
            username9,
        ).next_to(Recommend_group2, DOWN, buff=0.2)

        Recommend_group = Group(
            Recommend_group1,
            Recommend_group2,
            Recommend_group3
        )

        self.play(FadeIn(LOGO))
        duration = get_duration("./media/sounds/video_end.mp3")
        self.add_sound("./media/sounds/video_end.mp3", time_offset=0.5)
        self.play(Write(messages), run_rime=0.5)
        self.play(FadeIn(Recommend_group))
        self.wait(duration)
        self.play(FadeOut(Recommend_group,messages,LOGO))