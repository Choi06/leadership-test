import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 페이지 설정 ---
st.set_page_config(page_title="K-리더십 인사이트", layout="wide")

# UI 커스텀 스타일링
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #004a7c; color: white; font-weight: bold; }
    .leader-card {
        background-color: white; padding: 30px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-top: 20px;
        border-top: 8px solid #004a7c;
    }
    .motto { font-style: italic; color: #555; font-size: 1.3em; margin-bottom: 20px; text-align: center; }
    .hashtag { color: #007bff; font-weight: bold; font-size: 1.1em; margin-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 및 세션 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'survey_step' not in st.session_state:
    st.session_state.survey_step = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {}

leaders_info = {
    "Pioneer": {
        "name": "정주영 (현대)", "motto": "“시련은 있어도 실패는 없다.”",
        "bio": "가난한 농군의 아들로 태어나 현대그룹을 일궈낸 한국 경제의 상징.",
        "case": "유조선으로 물막이 공사를 성공시킨 '정주영 공법'과 경부고속도로 건설.",
        "hashtags": ["#실행력", "#불도저", "#현장중심"], "color": "#005aab"
    },
    "Architect": {
        "name": "이병철 (삼성)", "motto": "“인재제일(人才第一), 사업보국(사업보국).”",
        "bio": "치밀한 전략과 시스템으로 삼성을 글로벌 기업으로 키운 전략가.",
        "case": "삼성을 반도체 강국으로 만든 '도쿄 선언'과 무결점 인재 육성 시스템.",
        "hashtags": ["#시스템", "#데이터", "#선견지명"], "color": "#0047a0"
    },
    "Harmonizer": {
        "name": "구인회 (LG)", "motto": "“인화(人和)가 제일이다.”",
        "bio": "사람을 믿는 '인화 경영'으로 화학과 전자 산업의 기틀을 닦은 리더.",
        "case": "동업자와의 신뢰를 끝까지 지키며 잡음 없는 기업 문화를 정착시킴.",
        "hashtags": ["#인화", "#상생", "#신뢰경영"], "color": "#a50034"
    },
    "Steward": {
        "name": "박태준 (포스코)", "motto": "“짧은 인생을 영원한 조국에.”",
        "bio": "무결점 완벽주의로 포항제철의 신화를 쓴 강직한 사명가.",
        "case": "부실 공사 발견 시 구조물을 폭파하는 강단과 제철보국의 신념.",
        "hashtags": ["#사명감", "#무결점", "#원칙주의"], "color": "#434b54"
    }
}

questions = [
    {"q": f"{i+1}. 질문 내용...", "a": "A타입", "b": "B타입", "c": "C타입", "d": "D타입"} # 실제 20문항 데이터는 이전과 동일하게 유지
]
# 실제 20문항 리스트 (편의상 요약, 이전의 20문항을 그대로 넣으시면 됩니다)
from data_store import full_questions # 실제 구현 시에는 질문 리스트 전체 삽입

# --- 함수: 페이지 이동 ---
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 1. 시작 화면 (HOME) ---
if st.session_state.page == 'home':
    st.title("🇰🇷 K-Leadership Insight")
    st.subheader("대한민국 성장을 이끈 리더십의 비밀을 확인해보세요.")
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 1. 나의 리더십 모델 찾아보기"):
            st.session_state.survey_step = 1
            go_to('survey')
    with col2:
        if st.button("📚 2. 한국의 리더십 모델 알아보기"):
            go_to('dictionary')

# --- 2. 리더십 검사 (SURVEY) ---
elif st.session_state.page == 'survey':
    step = st.session_state.survey_step
    st.header(f"📊 리더십 검사 (단계: {step}/2)")
    
    # 1~10번 혹은 11~20번 문항 표시
    start_idx = 0 if step == 1 else 10
    end_idx = 10 if step == 1 else 20
    
    # 실제 20문항 리스트 (위에서 정의한 questions 사용)
    current_qs = full_questions[start_idx:end_idx] 
    
    for i, q in enumerate(current_qs):
        actual_idx = start_idx + i
        st.session_state.answers[actual_idx] = st.radio(
            q['q'], [q['a'], q['b'], q['c'], q['d']], 
            key=f"q{actual_idx}",
            index=None # 기본 선택 없음
        )
    
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("메인으로"): go_to('home')
    with col_next:
        if step == 1:
            if st.button("다음 페이지 (11~20번)"):
                st.session_state.survey_step = 2
                st.rerun()
        else:
            if st.button("결과 보기"):
                go_to('result')

# --- 3. 검사 결과 (RESULT) ---
elif st.session_state.page == 'result':
    st.header("🏆 당신의 리더십 분석 결과")
    
    # 점수 계산
    scores = {"Pioneer": 0, "Architect": 0, "Harmonizer": 0, "Steward": 0}
    for i in range(20):
        ans = st.session_state.answers.get(i)
        # 각 문항의 선택지와 리더 매칭 로직 (이전 코드와 동일)
        # ... (생략)

    res_type = "Pioneer" # 예시 결과
    leader = leaders_info[res_type]
    
    st.markdown(f"""<div class="leader-card">
        <h1 style='text-align: center;'>{leader['name']} 스타일</h1>
        <p class="motto">{leader['motto']}</p>
    </div>""", unsafe_allow_html=True)
    
    # 그래프 시각화 코드 (이전과 동일)
    # ...
    if st.button("다시 하기"): go_to('home')

# --- 4. 리더십 사전 (DICTIONARY) ---
elif st.session_state.page == 'dictionary':
    st.header("📚 한국형 리더십 사전")
    st.write("인물을 클릭하여 상세 내용을 확인하세요.")
    
    # 인물 선택 버튼 (상단 배치)
    cols = st.columns(4)
    selected_leader = st.session_state.get('selected_leader', "Pioneer")
    
    for i, (key, info) in enumerate(leaders_info.items()):
        if cols[i].button(info['name'].split(" ")[0]): # 이름만 표시
            st.session_state.selected_leader = key
            
    # 선택된 인물 상세 페이지
    info = leaders_info[st.session_state.get('selected_leader', 'Pioneer')]
    st.markdown(f"""
    <div class="leader-card">
        <h2>{info['name']}</h2>
        <p class="motto">{info['motto']}</p>
        <hr>
        <p><strong>📍 약력:</strong> {info['bio']}</p>
        <p><strong>💡 리더십 사례:</strong> {info['case']}</p>
        <p><strong>🏷️ 해시태그:</strong> {' '.join([f'<span class="hashtag">{t}</span>' for t in info['hashtags']])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("메인으로 돌아가기"): go_to('home')