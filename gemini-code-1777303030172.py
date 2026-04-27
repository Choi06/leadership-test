import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. 페이지 설정 및 디자인 (CSS) ---
st.set_page_config(page_title="K-리더십 인사이트", layout="wide")

st.markdown("""
    <style>
    /* 전체 배경: 종이 질감 */
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/paper-fibers.png");
        background-color: #f4f1ea;
    }
    
    /* 종이 설문지 스타일 */
    .paper-container {
        background-color: #ffffff;
        padding: 40px 50px;
        border-radius: 2px;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.1);
        border-left: 50px solid #e0e0e0;
        position: relative;
        margin-bottom: 30px;
    }
    .paper-container::before {
        content: '';
        position: absolute;
        top: 0; left: -50px; width: 50px; height: 100%;
        background-image: radial-gradient(#adb5bd 15%, transparent 20%);
        background-size: 50px 50px;
    }

    /* 백과사전 스타일 */
    .encyclopedia-box {
        background-color: #fffdf5;
        padding: 40px;
        border: 3px double #5d4037;
        border-radius: 10px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.05), 5px 5px 15px rgba(0,0,0,0.1);
        color: #3e2723;
    }
    .encyclopedia-title {
        text-align: center;
        border-bottom: 2px solid #5d4037;
        margin-bottom: 25px;
        padding-bottom: 10px;
        font-size: 2.2em;
        font-weight: bold;
    }

    /* 버튼 디자인 */
    .stButton>button {
        border-radius: 0px;
        border: 2px solid #5d4037;
        background-color: #ffffff;
        color: #5d4037;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #5d4037;
        color: white;
    }

    /* 해시태그 */
    .hashtag {
        background-color: #f0ebe0;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.9em;
        color: #5d4037;
        margin-right: 8px;
        border: 1px solid #dcd7ca;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 데이터 정의 ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'survey_step' not in st.session_state: st.session_state.survey_step = 1
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'selected_leader' not in st.session_state: st.session_state.selected_leader = 'Pioneer'

leaders_info = {
    "Pioneer": {
        "name": "정주영 (현대그룹)", "motto": "“이봐, 해봤어?”",
        "bio": "가난한 농군의 아들로 태어나 현대그룹을 일궈낸 실행력의 상징.",
        "case": "서산 간척지 유조선 물막이 공사와 500원권 거북선 지폐 차관 유치 일화.",
        "hashtags": ["#실행", "#불도저", "#현장주의"], "img": "https://upload.wikimedia.org/wikipedia/ko/c/c1/Chung_Ju-yung.jpg"
    },
    "Architect": {
        "name": "이병철 (삼성그룹)", "motto": "“인재제일(人才第一).”",
        "bio": "치밀한 전략과 시스템으로 삼성을 글로벌 기업으로 키운 전략가.",
        "case": "73세의 나이에 단행한 반도체 투자 결정으로 IT 강국의 기틀 마련.",
        "hashtags": ["#시스템", "#데이터", "#전략가"], "img": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Lee_Byung-chul.jpg"
    },
    "Harmonizer": {
        "name": "구인회 (LG그룹)", "motto": "“인화(人和)가 제일이다.”",
        "bio": "사람을 믿는 경영으로 화학과 전자 산업의 기틀을 닦은 리더.",
        "case": "동업자와의 신뢰를 수십 년간 유지하며 안정적인 기업 문화를 정착시킴.",
        "hashtags": ["#인화", "#상생", "#신뢰경영"], "img": "https://upload.wikimedia.org/wikipedia/ko/2/29/Koo_In-hwoi.jpg"
    },
    "Steward": {
        "name": "박태준 (포스코)", "motto": "“제철보국(製鐵報國).”",
        "bio": "무결점 완벽주의로 한국 철강 산업의 신화를 쓴 강직한 사명가.",
        "case": "부실 공사 구조물 폭파 사건과 헌신적인 포항제철 건설 과정.",
        "hashtags": ["#사명감", "#무결점", "#원칙주의"], "img": "https://upload.wikimedia.org/wikipedia/ko/d/d4/Park_Tae-joon.jpg"
    }
}

questions = [
    {"q": "1. 새로운 사업 기회가 보였을 때 당신의 첫 행동은?", "a": "일단 현장에 뛰어들어 시작한다", "b": "성공 가능성을 정밀하게 분석한다", "c": "함께 할 파트너를 먼저 찾는다", "d": "조직의 사명과 원칙에 부합하는지 본다"},
    {"q": "2. 목표 달성을 위해 가장 필요한 것은?", "a": "어떤 난관도 뚫고 나가는 뚝심", "b": "효율적인 시스템과 인재 배치", "c": "구성원들 간의 끈끈한 유대감", "d": "타협하지 않는 정직함과 완벽주의"},
    {"q": "3. '안 된다'는 반대에 부딪혔을 때 당신의 반응은?", "a": "직접 가능성을 증명해 보인다", "b": "논리적으로 설득할 데이터를 준비한다", "c": "충분한 대화로 상대의 마음을 돌린다", "d": "명분이 확실하다면 원칙대로 밀어붙인다"},
    {"q": "4. 일의 속도와 완성도 중 당신의 선택은?", "a": "일단 속도! 실행하며 수정한다", "b": "최적의 효율! 설계가 먼저다", "c": "조화! 모두가 납득할 때 진행한다", "d": "무결점! 속도보다 품질이 우선이다"},
    {"q": "5. 예상치 못한 큰 사고가 발생했을 때 대처 방식은?", "a": "현장에서 밤을 새우며 수습한다", "b": "원인 파악 후 재발 방지책을 세운다", "c": "피해자의 마음을 위로하고 중재한다", "d": "책임 소재를 명확히 하고 원칙대로 처리한다"},
    {"q": "6. 자금이 부족한 극한 상황이라면?", "a": "기발한 아이디어로 길을 만들어낸다", "b": "핵심 인재와 전략을 수정한다", "c": "신뢰를 바탕으로 외부 협력을 이끈다", "d": "사명감을 잃지 않고 정면 돌파한다"},
    {"q": "7. 조직 내부에 갈등이 생겼을 때?", "a": "강력한 리더십으로 목표에 정렬시킨다", "b": "인사 시스템을 조정해 원인을 제거한다", "c": "양측이 화해할 수 있는 자리를 마련한다", "d": "조직 기강을 위해 규정대로 처리한다"},
    {"q": "8. 자신의 판단이 틀렸음을 깨달았을 때?", "a": "즉시 인정하고 대안을 실행한다", "b": "분석을 통해 프로세스를 개선한다", "c": "주변의 조언을 수용하고 사과한다", "d": "결과에 책임을 지고 거취를 결정한다"},
    {"q": "9. 팀원을 뽑을 때 가장 중요한 덕목은?", "a": "패기와 근성", "b": "전문성과 분석력", "c": "인성과 배려", "d": "책임감과 정직"},
    {"q": "10. 부하 직원이 실수를 했을 때 교육 방식은?", "a": "혼내고 다시 도전할 기회를 준다", "b": "원인을 짚어주고 매뉴얼을 익히게 한다", "c": "다독이며 스스로 일어설 때까지 기다린다", "d": "공적 책임을 묻고 엄격히 훈계한다"},
    {"q": "11. 회의를 진행할 때 당신의 스타일은?", "a": "의견을 먼저 제시하고 동참을 구한다", "b": "전문가 보고를 듣고 최적안을 선택한다", "c": "편한 분위기에서 경청한다", "d": "절차를 명확히 하고 결론에 집중한다"},
    {"q": "12. 팀원들에게 동기를 부여하는 방법은?", "a": "성취감과 보상을 강조한다", "b": "개인의 성장 비전을 제시한다", "c": "소속감과 정을 나눈다", "d": "사회에 기여하는 명분을 강조한다"},
    {"q": "13. 당신에게 '성공'이란 무엇입니까?", "a": "남들이 못하는 것을 해내는 것", "b": "지속 가능한 일등 조직을 만드는 것", "c": "주변과 행복하게 공존하는 것", "d": "역사에 부끄럽지 않은 유산을 남기는 것"},
    {"q": "14. 수익보다 더 중요한 가치가 있다면?", "a": "끊임없는 도전 그 자체", "b": "최고의 인재를 키워내는 것", "c": "사람 사이의 믿음과 신의", "d": "공익을 위한 헌신과 청렴"},
    {"q": "15. 조직의 문화를 한 단어로 정의한다면?", "a": "도전 (Challenge)", "b": "인재 (Talent)", "c": "인화 (Harmony)", "d": "사명 (Mission)"},
    {"q": "16. 라이벌과의 경쟁에서 당신의 태도는?", "a": "공격적인 투자로 선점한다", "b": "기술력과 전략으로 제압한다", "c": "상생할 수 있는 길을 찾는다", "d": "도덕성과 실력으로 당당히 이긴다"},
    {"q": "17. 미래 트렌드를 예측하는 방법은?", "a": "현장을 발로 뛰며 체득한다", "b": "방대한 자료와 전문가 토론", "c": "인맥을 통해 흐름을 파악한다", "d": "역사와 시대적 소명에서 찾는다"},
    {"q": "18. 새로운 기술을 도입해야 할 때?", "a": "남보다 먼저 도입해 선점한다", "b": "효율성을 꼼꼼히 따져보고 도입한다", "c": "구성원들이 적응하도록 배려한다", "d": "윤리적 문제와 책임을 먼저 검토한다"},
    {"q": "19. 어떤 리더로 기억되고 싶나요?", "a": "불가능을 가능케 한 전설", "b": "기틀을 마련한 현명한 전략가", "c": "따뜻하고 좋았던 사람", "d": "대의를 위해 헌신한 참된 리더"},
    {"q": "20. 당신이 생각하는 진정한 리더십은?", "a": "앞장서서 이끄는 솔선수범", "b": "뒤에서 지원하는 시스템 경영", "c": "옆에서 함께 걷는 동행", "d": "위에서 중심을 잡는 원칙"}
]

# --- 3. 공통 함수 ---
def go_to(page_name):
    st.session_state.page = page_name
    st.rerun()

# --- 4. 페이지 렌더링 ---

# [1] 홈 화면
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align: center; color: #5d4037; font-size: 3.5em;'>📜 K-Leadership Index</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2em;'>대한민국 성장의 주역들, 당신은 어떤 리더의 심장을 가졌습니까?</p>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1542281286-9e0a16bb7366?q=80&w=2000", use_container_width=True)
    st.write("---")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 1. 나의 리더십 모델 찾아보기"): 
            st.session_state.survey_step = 1
            go_to('survey')
    with c2:
        if st.button("📚 2. 한국의 리더십 모델 알아보기"):
            go_to('dictionary')

# [2] 설문조사 (종이 스타일)
elif st.session_state.page == 'survey':
    step = st.session_state.survey_step
    st.markdown(f"<h2 style='text-align:center; color:#5d4037;'>📝 리더십 성향 조사지 ({step}/2)</h2>", unsafe_allow_html=True)
    
    st.markdown('<div class="paper-container">', unsafe_allow_html=True)
    start = 0 if step == 1 else 10
    for i in range(start, start + 10):
        q_item = questions[i]
        st.write(f"**Q{i+1}. {q_item['q']}**")
        st.session_state.answers[i] = st.radio("선택", [q_item['a'], q_item['b'], q_item['c'], q_item['d']], key=f"q{i}", label_visibility="collapsed")
        st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("메인으로"): go_to('home')
    with c2:
        if step == 1:
            if st.button("다음 페이지 (11~20번)"): st.session_state.survey_step = 2; st.rerun()
        else:
            if st.button("결과 확인하기"): go_to('result')

# [3] 결과 확인 (3페이지)
elif st.session_state.page == 'result':
    st.markdown("<h2 style='text-align:center; color:#5d4037;'>🏆 분석 결과 리포트</h2>", unsafe_allow_html=True)
    
    scores = {"Pioneer": 0, "Architect": 0, "Harmonizer": 0, "Steward": 0}
    for i in range(20):
        ans = st.session_state.answers.get(i)
        if ans == questions[i]['a']: scores["Pioneer"] += 1
        elif ans == questions[i]['b']: scores["Architect"] += 1
        elif ans == questions[i]['c']: scores["Harmonizer"] += 1
        elif ans == questions[i]['d']: scores["Steward"] += 1
    
    res_type = max(scores, key=scores.get)
    leader = leaders_info[res_type]
    
    st.markdown(f"""
    <div class="encyclopedia-box">
        <h1 style='text-align: center; color: #5d4037;'>당신은 [{leader['name']}] 형 리더입니다.</h1>
        <p style='text-align: center; font-style: italic; font-size: 1.3em;'>"{leader['motto']}"</p>
        <hr style='border: 1px solid #5d4037;'>
        <p><b>성향 분석:</b> {leader['bio']}</p>
        <p><b>핵심 키워드:</b> {' '.join([f'<span class="hashtag">{t}</span>' for t in leader['hashtags']])}</p>
    </div>
    """, unsafe_allow_html=True)
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[scores['Pioneer'], scores['Architect'], scores['Harmonizer'], scores['Steward']],
        theta=['개척(정주영)', '설계(이병철)', '화합(구인회)', '원칙(박태준)'],
        fill='toself', fillcolor='rgba(93, 64, 55, 0.3)', line=dict(color='#5d4037')
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
    st.plotly_chart(fig)
    
    if st.button("다시 검사하기"): go_to('home')

# [4] 인물 사전 (백과사전 스타일)
elif st.session_state.page == 'dictionary':
    st.markdown("<h2 style='text-align:center; color:#5d4037;'>📚 인물 대백과사전</h2>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    btn_names = ["정주영", "이병철", "구인회", "박태준"]
    keys = ["Pioneer", "Architect", "Harmonizer", "Steward"]
    for i in range(4):
        if cols[i].button(btn_names[i]):
            st.session_state.selected_leader = keys[i]
            
    info = leaders_info[st.session_state.selected_leader]
    st.markdown('<div class="encyclopedia-box">', unsafe_allow_html=True)
    st.markdown(f'<div class="encyclopedia-title">{info["name"]}</div>', unsafe_allow_html=True)
    
    col_img, col_txt = st.columns([1, 2])
    with col_img:
        st.image(info['img'], caption=info['name'], use_container_width=True)
    with col_txt:
        st.markdown(f"### {info['motto']}")
        st.write(f"**[약력]** \n{info['bio']}")
        st.write(f"**[리더십 사례]** \n{info['case']}")
        st.markdown(f"**[키워드]** \n{' '.join([f'<span class=\"hashtag\">{t}</span>' for t in info['hashtags']])}", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    if st.button("메인 화면으로"): go_to('home')