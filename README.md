# Streamlit AI 챗봇

OpenAI API의 `gpt-4o-mini`를 사용하는 간단한 한국어 채팅 앱입니다.

## Streamlit Community Cloud 배포

1. 이 폴더를 GitHub 저장소에 올리고 Streamlit Community Cloud에서 앱을 배포합니다.
2. 앱의 **Settings → Secrets**에 다음을 입력합니다.

   ```toml
   OPENAI_API_KEY = "발급받은 OpenAI API 키"
   ```

3. 앱을 재시작합니다. 키는 저장소에 커밋하지 마세요.

## 로컬 실행

```bash
python -m pip install -r requirements.txt
```

환경 변수 `OPENAI_API_KEY`를 설정한 뒤 다음 명령으로 실행합니다.

```bash
streamlit run app.py
```

또는 `.streamlit/secrets.toml` 파일을 만들고 같은 TOML 설정을 넣을 수 있습니다. 이 파일은 `.gitignore`에 포함되어 있습니다.
