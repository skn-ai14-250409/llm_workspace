from dotenv import load_dotenv
# load_dotenv() # .env 내용을 읽어서 환경변수로 설정 -> 클라우드에서 돌아갈경우 필요가 없음, 로컬만 !
                # 왜? streamlit-cloud 에서는 .evn 를 올릴 수 없으니까 !!
                # 그래서 실제 로컬에 올릴땐 스트림릿 웹사이트 secrets((TOML) 설정에  OPENAI_API_KEY 를 설정해야함
                # OPENAI_API_KEY='키' 이렇게 적어놓으면 자동으로 리눅스 버전으로 등록을 해줌

from openai import OpenAI
import os
import base64


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
    filename = 'voice.mp3'
    with client.audio.speech.with_streaming_response.create(
        model='tts-1',
        voice='alloy',
        input=response # 텍스트
    ) as stream :
        stream.stream_to_file(filename)

    # 음원을 base64 문자열로 인코딩 처리
    with open(filename,'rb') as f:
        data = f.read()
        base64_encoded = base64.b64encode(data).decode() # 인코딩하고 디코딩해야 텍스트로 나옴

    # 반환해주기 전에 음원파일 삭제
    os.remove(filename)
    return base64_encoded
