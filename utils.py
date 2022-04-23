import librosa
import re

def cut(obj: str, sec: int=40) -> list:
    """cut the string into list

    Args:
        obj (str): text need to be cut
        sec (int, optional): words count. Defaults to 40.

    Returns:
        list: list of words
    """
    obj.strip()
    str_list = [obj[i:i+sec] for i in range(0,len(obj),sec)]
    print(str_list)
    return str_list

def get_duration(file_path: str) -> float:
    """get duration of mp3 file

    Args:
        file_path (str): mp3 file path

    Returns:
        float: duration of mp3 file
    """
    duration = librosa.get_duration(filename=file_path)
    return duration

def deal_text(text: str) -> str:
    """deal the text

    Args:
        text (str): text need to be deal

    Returns:
        str: dealed text
    """
    text = "    "+text
    text = text.replace("。","。\n    ")
    text = text.replace("？","？\n    ")
    text = text.replace("！","！\n    ")
    text = text.replace("；","；\n    ")
    return text
