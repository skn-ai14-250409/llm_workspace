# from dotenv import load_dotenv
# load_dotenv()
# streamlit-cloud 에서는 .env 를 사용할 수 없으므로,
# secrets 설정에 TOML 형식으로 OPENAI_API_KEY 등 환경변수를 따로 설정해줘야 한다.
# 예) OPENAI_API_KEY="이 안에 키값"

from openai import OpenAI
import base64
import os


# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()

def stt(audio):
    filename = "prompt.mp3"
    audio.export(filename, format="mp3")

    with open("prompt.mp3", "rb") as f:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
        )

    # 임시로 만든 음원파일 삭제
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
    filename = "voice.mp3"
    params = {
        "model"     : "tts-1",
        "voice"     : "nova",
        "input"     : response
    }
    with client.audio.speech.with_streaming_response.create(**params) as stream:
        stream.stream_to_file(filename)

    # 음원을 Base64 로 인코딩
    with open(filename, "rb") as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode()

    # 다 사용한 음원파일은 삭제
    os.remove(filename)

    return base64_encoded