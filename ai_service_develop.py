import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key = st.secrets["OPEN_API_KEY"]
)

st.title("🧑‍🏫 십대랑 대화하는 거 쉽대")
st.subheader("할아버지! 제가 알려드릴게요🐣")

auto_complete = st.toggle(label="예시로 채우기")
example = {
    "name" : "캘박"
}

def generate_prompt(m_z_lan):
    system_message = f"""
아래 신조어 사전을 참고해서 유저에게 신조어의 의미를 알려주세요.
아이가 할아버지에게 설명하는 어투로 설명해주세요.
재밌는 예시도 이모지를 적절히 섞어서 2개 제시해주세요.
만약 제시된 신조어가 아니라면, 정중히 틀렸음을 명시해주세요.

캘박: 캘린더 박제의 의미로 일정을 확정한다는 뜻
스불재: 스스로 불러온 재앙의 줄임말로 너무 많은 욕심을 부려서 스스로를 고통스럽게 하는 사람을 이름
편디족: 편의점 디저트를 즐기는 사람을 이름
카공족: 카페를 학습공간으로 사용하는 사람을 이름
폼 미쳤다: 기량이 매우 뛰어나다는 뜻
좋댓구알: 좋아요, 댓글, 구독, 알림설정의 줄임말
일며들다: 일이 내 삶에 스며들었다는 뜻
중꺾마: 중요한 건 꺾이지 않는 마음의 줄임말
싫존주의: 싫어하는 것을 존중하자는 주의
갓생: God(갓)+인생, 성실하고 부지런하여 성공한 삶
돼지런하다: 평소에는 게으른데 먹을 때만 부지런하다는 의미
저메추: 저녁 메뉴 추천 줄임말
사바사: 사람 바이 사람 줄임말, 사람에 따라 다르다는 의미
케바케: 케이스 바이 케이스 줄임말, 상황에 따라 다르다는 의미
꾸안꾸: 꾸민듯 안 꾸민듯 줄임말, 수수하게 이쁘다는 것을 의미
그잡채: 그 자체 
꾸웨엑: 후회해
돔황챠: 도망쳐
억텐: 억지 텐션을 뜻함
자낳괴: 자본주의가 낳은 괴물이라고 정이 없고 돈을 추구하는 사람을 이름
---
신조어:{m_z_lan}
---
    """.strip()
    return system_message

def request_chat_completion(system_message):
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{name}은 무슨 뜻이야?"}
        ],
        stream=True
    )
    return response

def print_streaming_response(response):
    message = ""
    placeholder = st.empty()
    for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            message += delta.content
            placeholder.markdown(message + "▌")
    placeholder.markdown(message)

with st.form("form"):
    name = st.text_input(
        "알고 싶은 신조어(필수)",
        value=example["name"] if auto_complete else "",
        placeholder=example["name"])
    submit = st.form_submit_button("제출하기")
if submit:
    if not name:
        st.error("알고 싶은 신조어를 입력해 주세요.")
    else:
        system_message = generate_prompt(
            m_z_lan=name)
        response = request_chat_completion(system_message)
        print_streaming_response(response)