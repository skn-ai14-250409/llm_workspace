1. 일단, 소스는 streamlit 에서 보이는 대로, 말로 한걸 녹음하면 그걸 stt - openai - tts 로 바꿔서 대화형 챗봇처럼 동작하게 만드는거.
2. 여기에는 OS 레벨에서 설치한 ffmpeg 이 필요한데,
  1. 이게 streamlit-cloud 환경에는 설치가 안되어있을거기 때문에, packages.txt 파일을 만들어서 알려줘야 한다.
3. 그러고나서<br/>
   ```commandline
   pip list --format=freeze | findstr /V "win32 pypiwin32 pywin32 pywinauto pywinpty" > requirements.txt
   ```
   이걸로 python 에 필요한 패키지 목록을 명시해줘야 한다.
4. requirements.txt 에 windows 관련 패키지는 없는지 확인하고, 있으면 삭제해야 streamlit-cloud 에 배포할 수 있다.
5. 여기서는 dotenv 도 사용했는데, 마찬가지로 이 환경변수들도 streamlit-cloud 에 없을거기 때문에, secrets 설정에 TOML 형식으로 OPENAI_API_KEY 등 환경변수를 따로 설정해줘야 한다.