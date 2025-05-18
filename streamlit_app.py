import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
import io
import textwrap
import re
import openai

# OpenAI API 키를 secrets에서 불러오기
openai_api_key = st.secrets["OPENAI_API_KEY"]

st.title("PPT 자동 생성기 (Streamlit)")

st.markdown('''
내용을 단락락별로 번호로 구분해서 정리해서 넣기 (예: 1. 사업의 필요성 2. 사업의 개요 ... 5. 기대효과 형태로)
''')

st.markdown("""
**내용 입력**  
""")

# 1. 입력
content = st.text_area("PPT로 만들고 싶은 내용을 입력하세요...", height=200)

# 2. 요약 생성 버튼
if st.button("요약 생성"):
    # 슬라이드별로 분할 (번호. 제목\n내용)
    items = re.findall(r'(\d+)\.\s*([^\n]+)\n([^\n]+(?:\n(?!\d+\.).+)*)', content, re.MULTILINE)
    slides_content = []
    client = openai.OpenAI(api_key=openai_api_key)
    for idx, title, item_content in items:
        # OpenAI로 요약
        prompt = f"다음 내용을 2~3줄의 bullet point로 요약해줘:\n{item_content.strip()}"
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.7,
            )
            summary = response.choices[0].message.content.strip()
        except Exception as e:
            summary = f"(요약 실패: {e})\n{item_content.strip()}"
        slides_content.append({'title': title.strip(), 'content': summary})

    st.session_state['slides_content'] = slides_content

# 3. 슬라이드별 미리보기/수정
if 'slides_content' in st.session_state:
    st.markdown("**슬라이드별 내용 미리보기 및 수정**")
    edited_slides = []
    for i, slide in enumerate(st
