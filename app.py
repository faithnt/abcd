import os

import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="AI 챗봇",
    page_icon="💬",
    layout="centered",
)


def get_api_key() -> str | None:
    """Read the API key from Streamlit Secrets or a local environment variable."""
    try:
        secret_key = st.secrets.get("OPENAI_API_KEY")
    except (AttributeError, KeyError, FileNotFoundError):
        secret_key = None
    return secret_key or os.getenv("OPENAI_API_KEY")


st.title("💬 AI 챗봇")
st.caption("OpenAI API와 gpt-4o-mini로 대화해 보세요.")

api_key = get_api_key()
if not api_key:
    st.info(
        "아직 OpenAI API 키가 설정되지 않았습니다. "
        "Streamlit Community Cloud 앱의 **Settings → Secrets**에 "
        '`OPENAI_API_KEY = "발급받은 키"` 를 추가해 주세요.'
    )
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("대화 설정")
    system_prompt = st.text_area(
        "챗봇 안내 문구",
        value="당신은 친절하고 정확하게 답변하는 한국어 AI assistant입니다.",
        help="대화의 말투와 역할을 지정합니다.",
    )
    if st.button("대화 내용 지우기", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("사용 모델: gpt-4o-mini")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_area = st.empty()
        answer = ""
        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    *st.session_state.messages,
                ],
                stream=True,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                answer += token
                response_area.markdown(answer + "▌")
            response_area.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
        except Exception as error:
            # Avoid displaying request details or credentials in the chat UI.
            response_area.error(
                "응답을 가져오지 못했습니다. API 키와 OpenAI 프로젝트의 사용량 한도를 확인한 뒤 다시 시도해 주세요."
            )
