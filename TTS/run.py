from TTS.TTS import mainSeq
import asyncio

def get_mp3_file(path):
    with open(path,'r',encoding='utf-8') as f:
        return f.read()


asyncio.get_event_loop().run_until_complete(mainSeq(SSML_text, output_path))