import streamlit as st
from audiorecorder import audiorecorder
from openai_service import stt, ask_gpt, tts

# from dotenv import load_dotenv
# from openai import OpenAI
# import os
# import base64
#
# load_dotenv() # .env 내용을 읽어서 환경변수로 설정
#
# client = OpenAI() # api_key는 환경변수에 있으므로 생략가능
#
#
#
#
# def stt(audio):
#     # 파일로 변환
#     filename = 'prompt.mp3'
#     audio.export(filename, format='mp3')
#
#     # whisper-1 모델로 stt
#     with open(filename, 'rb') as f:
#         transcription = client.audio.transcriptions.create(
#             model='whisper-1',
#             file=f
#         )
#     # 임시음원파일 삭제
#     os.remove(filename)
#     return transcription.text
#
# def ask_gpt(messages, model):
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=1,
#         top_p=1,
#         max_tokens=4096
#     )
#     return response.choices[0].message.content
#
# def tts(response):
#     filename='voice.mp3'
#     with client.audio.speech.with_streaming_response.create(
#         model = 'tts-1',
#         voice = 'alloy',
#         input=response
#
#     ) as stream:
#         stream.stream_to_file(filename)
#     # 음원을 base64 문자열로 인코딩 처리
#     with open(filename, 'rb') as f:
#         data = f.read()
#         base64_encoded=base64.b64encode(data).decode()
#     # 음원파일 삭제
#     #os.remove(filename)
#     return base64_encoded


def main():
    st.set_page_config(
        page_title='😎Voice Chatbot😎',
        page_icon="🎤",
        layout='wide'
    )
    st.header('🎤Voice Chatbot🎤')
    st.markdown('---')

    with st.expander('Voice Chatbot 프로그램 처리절차', expanded=False):
        st.write(
            """
            1. 녹음하기 버튼을 눌러 질문을 녹음합니다.
            2. 녹음이 완료되면 자동으로 Whisper모델을 이용해 음성을 텍스트로 변환합니다. 
            3. 변환된 텍스트로 LLM에 질의후 응답을 받습니다.
            4. LLM의 응답을 다시 TTS모델을 사용해 음성으로 변환하고 이를 사용자에게 들려줍니다.
            5. 모든 질문/답변은 채팅형식의 텍스트로 제공합니다.
            """
        )
    if 'messages' not in st.session_state:
        st.session_state['messages'] = [
            {'role':'system', 'content':'당신은 친절한 챗봇입니다.'}
        ]
    if 'check_reset' not in st.session_state:
        st.session_state['check_reset'] = False

    with st.sidebar:
        model = st.radio(label='GPT 모델', options=['gpt-4.1', 'gpt-4o', 'gpt-4o-mini'], index=2)
        print(f'model={model}')

        if st.button(label='초기화'):
            st.session_state['check_reset'] = True
            st.session_state['messages'] = [
                {'role': 'system', 'content': '당신은 친절한 챗봇입니다.'}
            ]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('녹음하기')
        audio = audiorecorder()
        if (audio.duration_seconds>0) and (not st.session_state['check_reset']):
            # 음원 재생
            st.audio(audio.export().read())
            #st.session_state['check_reset'] = True

            # stt 사용자 프롬프트 추출
            prompt = stt(audio)
            print(f'prompt={prompt}')

            # chat completion 호출
            # - messages에 추가
            st.session_state['messages'].append({'role':'user', 'content':prompt})
            # - llm 요청
            response = ask_gpt(st.session_state['messages'], model)
            st.session_state['messages'].append({'role': 'assistant', 'content': response})
            print(f'response={response}')


            # llm 응답을 tts 모델을 통해 음원파일로 변환/재생
            base64_encoded = tts(response)
            #print(base64_encoded)
            st.html(f'''
            <audio>
            #<audio autoplay='true'>
                <source src='data:audio/mp3;base64,{base64_encoded}' type='audio/mp3'/>
            </audio>
            ''')



        #print(audio.duration_seconds)
    with col2:
        st.subheader('질문/답변')
        if (audio.duration_seconds>0) and (not st.session_state['check_reset']):
            for message in st.session_state['messages']:
                role = message['role'] # system/user/assistant
                content = message['content']

                if role == 'system':
                    continue
                # elif role == 'user':
                #     st.session_state['messages'].append({'role': 'assistant', 'content': response})

                #else:

                with st.chat_message(role):
                    st.markdown(content)

        else:
            st.session_state['check_reset'] =False #초기화상태 값은 원복



if __name__ == '__main__':
    main()