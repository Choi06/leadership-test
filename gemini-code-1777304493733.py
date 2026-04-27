import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 1. 앱 스타일 세팅 (Native App UI CSS) ---
st.set_page_config(page_title="K-Leadership Insight", layout="centered")

st.markdown("""
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
<style>
    /* 전체 레이아웃 및 폰트 */
    html, body, [class*="st-"] {
        font-family: 'Pretendard', -apple-system, sans-serif;
        color: #1A1A1A !important;
        word-break: keep-all;
    }
    .stApp { background-color: #F8F9FB; }

    /* 1. 시작 화면 Full-Screen Hero */
    .hero-section {
        background-image: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                          url("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2000");
        background-size: cover; background-position: center;
        height: 450px; display: flex; flex-direction: column;
        justify-content: center; align-items: center;
        border-radius: 0 0 40px 40px; margin: -6rem -2rem 2rem -2rem;
        color: white; text-align: center;
    }

    /* 2. 설문지 둥근 사각형 카드 */
    .q-card {
        background-color: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
        border: 1px solid #EAECEF;
        margin-bottom: 10px;
        margin-top: 20px;
    }
    .q-title { font-weight: 800; font-size: 1.15rem; color: #004A7C; margin-bottom: 10px; }

    /* 3. 백과사전 카드 스타일 */
    .bio-card {
        background-color: white;
        padding: 30px;
        border-radius: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.07);
        border: 1px solid #F0F0F0;
    }
    .bio-section-title {
        font-size: 1.1rem; font-weight: 700; color: #004A7C;
        margin-top: 25px; margin-bottom: 10px;
        border-left: 5px solid #004A7C; padding-left: 12px;
    }

    /* 버튼 스타일 */
    .stButton>button {
        width: 100%; border-radius: 18px !important;
        border: none !important; background-color: #004A7C !important;
        color: white !important; height: 4rem;
        font-weight: 700; font-size: 1.1rem;
        box-shadow: 0 10px 20px rgba(0,74,124,0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:active { transform: scale(0.98); }
</style>
""", unsafe_allow_html=True)

# --- 2. 보강된 리더십 데이터 ---
leaders_info = {
    "Pioneer": {
        "name": "정주영 (현대그룹)",
        "motto": "“시련은 있어도 실패는 없다.”",
        "bio": "강원도 통천의 가난한 농군으로 태어나 소 판 돈 70원을 들고 가출한 소년이 현대그룹을 일궈냈습니다. '해보기나 했어?'라는 한마디로 한국의 불가능을 가능으로 바꾼 실행력의 화신입니다.",
        "case": "• **서산 간척지 정주영 공법**: 거센 물살로 방조제 물막이 공사가 한계에 부딪히자, 거대한 폐유조선을 침몰시켜 물길을 막는 기상천외한 공법으로 세계 건설사를 새로 썼습니다.\n\n• **조선소 건립 차관 유치**: 영국 은행가들을 설득하기 위해 500원권 지폐의 거북선 그림을 보여주며 '우리는 당신들보다 300년이나 앞서 철갑선을 만들었다'고 호언장담하여 차관을 따낸 일화는 유명합니다.",
        "hashtags": ["#불굴의_도전", "#현장_우선", "#창의적_실행"],
        "img": "https://img.khan.co.kr/news/2021/03/18/l_2021031901002347300185931.jpg"
    },
    "Architect": {
        "name": "이병철 (삼성그룹)",
        "motto": "“인재제일(人才第一), 사업보국(事業報國).”",
        "bio": "치밀한 분석력과 시스템을 기반으로 삼성을 글로벌 초일류 기업으로 성장시켰습니다. '기업은 곧 사람'이라는 철학으로 인재를 귀하게 여겼으며, 무결점 시스템 경영의 기틀을 닦았습니다.",
        "case": "• **2.8 도쿄 선언**: 1983년, 모두가 불가능하다고 했던 고령의 나이에 반도체 산업 진출을 선언했습니다. 철저한 분석과 미래 예측을 통해 오늘날 IT 강국 대한민국의 근간을 마련했습니다.\n\n• **인재 경영 시스템**: 한국 기업 최초로 공채 제도를 도입하고, '의심스러운 사람은 쓰지 말고, 쓴 사람은 의심하지 말라'는 철저한 능력 중심의 용인술을 실천했습니다.",
        "hashtags": ["#시스템_경영", "#미래_선견지명", "#인재_중심"],
        "img": "https://upload.wikimedia.org/wikipedia/commons/e/e0/Lee_Byung-chul.jpg"
    },
    "Harmonizer": {
        "name": "구인회 (LG그룹)",
        "motto": "“한 번 믿으면 끝까지 믿는다. 인화(人和)가 제일이다.”",
        "bio": "유교적 가풍 속에서 화합과 상생을 중시했습니다. 락희화학(LG화학)과 금성사(LG전자)를 세우며 한국의 기초 화학 및 가전 산업을 일궈낸 '인화'의 리더입니다.",
        "case": "• **허씨 가문과의 상생**: 수십 년간 지속된 허씨 가문과의 동업 관계를 잡음 하나 없이 성공적으로 이끌었습니다. 이는 한국 기업사에서 '신뢰와 상생'의 리더십이 거둔 가장 큰 승리로 평가받습니다.\n\n• **불모지 개척 정신**: 모두가 기술 없이는 불가능하다고 했던 시절, 라디오와 세탁기 등 국산 가전제품을 최초로 생산하며 국민의 삶을 혁신적으로 바꿨습니다.",
        "hashtags": ["#상생_협력", "#인화_리더십", "#신뢰_경영"],
        "img": "https://img.hankyung.com/pdsdata/prplus/65/201601/20160126135835_534887_1.jpg"
    },
    "Steward": {
        "name": "박태준 (포스코)",
        "motto": "“짧은 인생을 영원한 조국에. 제철보국(製鐵報國).”",
        "bio": "군인의 강직함과 청렴함으로 무장한 리더였습니다. 황량한 영일만 모래벌판에서 '무에서 유를 창조한다'는 일념으로 세계 최고의 제철소를 건설한 강직한 사명가입니다.",
        "case": "• **무결점 폭파 일화**: 포항제철 건설 도중 부실 공사가 발견되자, 이미 거의 완성된 구조물을 단호하게 폭파하고 다시 짓게 했습니다. 타협 없는 완벽주의가 세계 1위 제철소의 근간이 되었습니다.\n\n• **제철보국 정신**: '철을 만들어 나라에 보답한다'는 신념으로, 단 1원도 개인의 이익으로 취하지 않고 오직 국가 발전만을 위해 헌신한 청렴의 표상입니다.",
        "hashtags": ["#사명감", "#청렴_강직", "#완벽주의"],
        "img": "https://upload.wikimedia.org/wikipedia/ko/d/d4/Park_Tae-joon.jpg"
    }
}

# --- 3. 20문항 데이터 ---
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

# --- 4. 세션 상태 및 로직 ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'survey_step' not in st.session_state: st.session_state.survey_step = 1
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'final_results' not in st.session_state: st.session_state.final_results = None
if 'selected_leader' not in st.session_state: st.session_state.selected_leader = 'Pioneer'

def go_to(page):
    st.session_state.page = page
    st.rerun()

# --- 5. 화면 렌더링 ---

# [HOME]
if st.session_state.page == 'home':
    st.markdown("""
        <div class="hero-section">
            <h1 style='font-size: 3.2rem; font-weight: 900; margin-bottom: 5px;'>K-Leadership</h1>
            <p style='font-size: 1.2rem; opacity: 0.8;'>역사를 바꾼 거인들의 리더십 인사이트</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>"*2, unsafe_allow_html=True)
    if st.button("🔍 1. 나의 리더십 모델 찾아보기"): 
        st.session_state.survey_step = 1
        go_to('survey')
    st.write("")
    if st.button("📚 2. 한국형 리더십 대백과사전"): 
        go_to('dictionary')

# [SURVEY]
elif st.session_state.page == 'survey':
    step = st.session_state.survey_step
    st.markdown(f"### 📋 리더십 성향 분석 ({step}/2)")
    st.progress(step * 0.5)
    
    start = 0 if step == 1 else 10
    for i in range(start, start + 10):
        q_item = questions[i]
        st.markdown(f"""
            <div class="q-card">
                <div class="q-title">QUESTION {i+1}</div>
                <div style='font-weight: 700; line-height: 1.5;'>{q_item['q']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.session_state.answers[i] = st.radio(
            "선택지", [q_item['a'], q_item['b'], q_item['c'], q_item['d']], 
            key=f"q{i}", label_visibility="collapsed"
        )
        st.write("")

    col1, col2 = st.columns(2)
    if col1.button("처음으로"): go_to('home')
    if step == 1:
        if col2.button("다음 페이지 ➡️"): 
            st.session_state.survey_step = 2
            st.rerun()
    else:
        if col2.button("분석 결과 확인 🏆"):
            s = {"Pioneer": 0, "Architect": 0, "Harmonizer": 0, "Steward": 0}
            for j in range(20):
                ans = st.session_state.answers.get(j)
                if ans == questions[j]['a']: s["Pioneer"] += 1
                elif ans == questions[j]['b']: s["Architect"] += 1
                elif ans == questions[j]['c']: s["Harmonizer"] += 1
                elif ans == questions[j]['d']: s["Steward"] += 1
            st.session_state.final_results = s
            go_to('result')

# [RESULT]
elif st.session_state.page == 'result':
    st.header("🏆 리더십 분석 리포트")
    res = st.session_state.final_results
    res_type = max(res, key=res.get)
    leader = leaders_info[res_type]
    
    st.markdown(f"""
        <div class="bio-card">
            <h2 style='color:#004A7C; margin-bottom:0;'>{leader['name']} 스타일</h2>
            <p style='font-style:italic; color:#666; font-size:1.2rem; margin-top:5px;'>"{leader['motto']}"</p>
            <hr>
            <p style='line-height:1.7;'>{leader['bio']}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 레이더 차트 (고정 설정)
    fig = go.Figure(data=go.Scatterpolar(
        r=[res['Pioneer'], res['Architect'], res['Harmonizer'], res['Steward']],
        theta=['개척(정주영)', '설계(이병철)', '화합(구인회)', '원칙(박태준)'],
        fill='toself', fillcolor='rgba(0, 74, 124, 0.4)', line=dict(color='#004A7C')
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
    st.plotly_chart(fig, config={'staticPlot': True}, use_container_width=True)
    
    if st.button("홈으로 돌아가기"): go_to('home')

# [DICTIONARY]
elif st.session_state.page == 'dictionary':
    st.header("📚 리더십 대백과사전")
    
    # 상단 탭 스타일 선택
    tabs = st.columns(4)
    names = ["정주영", "이병철", "구인회", "박태준"]
    keys = ["Pioneer", "Architect", "Harmonizer", "Steward"]
    for i in range(4):
        if tabs[i].button(names[i]): st.session_state.selected_leader = keys[i]
            
    info = leaders_info[st.session_state.selected_leader]
    
    st.markdown(f"""
        <div class="bio-card">
            <h2 style='text-align:center; color:#004A7C; margin-bottom:20px;'>{info['name']}</h2>
            <img src="{info['img']}" style='width:100%; border-radius:20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); margin-bottom:30px;'>
            <div class="bio-section-title">📍 생애와 철학</div>
            <p style='line-height:1.7;'>{info['bio']}</p>
            <div class="bio-section-title">💡 리더십 성공 사례</div>
            <p style='line-height:1.7; white-space: pre-wrap;'>{info['case']}</p>
            <div class="bio-section-title">🏷️ 핵심 키워드</div>
            <p style='font-weight:700; color:#555;'>{"  ".join(info['hashtags'])}</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("홈으로 돌아가기"): go_to('home')