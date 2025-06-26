# streamlit-cloud에서는 .env를 사용할 수 없으므로,
# secrets설정(TOML)에 OPENAI_API_KEY를 설정해야 한다.


import base64
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import os


load_dotenv(dotenv_path=find_dotenv())   # .env 내용을 읽어서 환경변수로 설정
print(find_dotenv())
print(os.getenv("OPENAI_API_KEY"))

client = OpenAI()

def stt(audio):
    # 파일로 변환
    filename = 'prompt.mp3'
    audio.export(filename, format='mp3')

    # whisper-1 모델로 stt
    with open(filename, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model='whisper-1',
            file=f
        )
    # 음원파일 삭제
    os.remove(filename)
    return transcription.text

def ask_gpt(messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=1,
        top_p=1,
        max_tokens=4096
    )
    return response.choices[0].message.content

def tts(response):
    file_name = 'voice.mp3'
    with client.audio.speech.with_streaming_response.create(
        model='tts-1',
        voice='alloy',
        input=response
    ) as stream:
        stream.stream_to_file(file_name)

    # 음원을 base64문자열로 인코딩처리
    with open(file_name, 'rb') as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()
    # 음원파일 삭제
    os.remove(file_name)
    return base64_encoded

