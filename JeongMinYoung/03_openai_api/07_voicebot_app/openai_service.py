from audiorecorder import audiorecorder
from dotenv import load_dotenv
from openai import OpenAI
import os
import base64

# load_dotenv() # .env의 내용을 읽어서 환경변수로 설정
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def stt(audio):
    # 파일로 변환
    filename = 'prompt.mp3'
    audio.export(filename, format='mp3')

    # whipser-1 모델로 stt
    with open(filename, 'rb') as f:
        transcription = client.audio.transcriptions.create(
            model = 'whisper-1',
            file = f
        )

    # 음원파일 삭제
    os.remove(filename)

    return transcription.text


def ask_gpt(prompt, model):
    response = client.chat.completions.create(
    model = model,
    messages=prompt,
        top_p=1,
        temperature=0.8,
        max_tokens=1000)

    return response.choices[0].message.content

def tts(response):
    filename = 'voice.mp3'
    with client.audio.speech.with_streaming_response.create(
        model='tts-1',
        voice='alloy',
        input=response
    ) as stream:
        stream.stream_to_file(filename)

    # 음원을 base64문자열로 인코딩
    with open(filename, 'rb') as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()
    # 움원 파일 삭제
    os.remove(filename)
    return base64_encoded