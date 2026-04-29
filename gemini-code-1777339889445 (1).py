import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os
import base64

# --- 사진을 읽어서 CSS에 넣을 수 있게 변환하는 함수 ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 메인 사진 파일 경로 확인 및 변환
hero_img_path = "images/main_hero.jpg"
if os.path.exists(hero_img_path):
    bin_str = get_base64_of_bin_file(hero_img_path)
    hero_bg_style = f"url('data:image/jpg;base64,{bin_str}')"
else:
    hero_bg_style = "linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5))"

# --- 1. 앱 스타일 세팅 ---
st.set_page_config(page_title="K-Leadership Insight", layout="centered")

# --- 여기에 추가: 깃허브 아이콘 및 메뉴 숨기기 ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --------------------------------------------
st.markdown(f"""
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
<style>
    html, body, [class*="st-"] {{
        font-family: 'Pretendard', sans-serif;
        color: #1A1A1A !important;
        word-break: keep-all;
    }}
    .stApp {{ background-color: #F8F9FB; }}
    
    .hero-section {{
        background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                          {hero_bg_style};
        background-size: contain; 
        background-repeat: no-repeat;
        background-position: center;
        height: 250px !important; 
        display: flex; 
        flex-direction: column;
        justify-content: center; 
        align-items: center;
        border-radius: 25px !important; 
        margin: 10px auto !important; 
        width: 95%; 
        color: white !important; 
        text-align: center; 
        padding: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }}
    
    .hero-section h1 {{
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin-bottom: 5px !important;
        color: white !important;
        text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
    }}

    .hero-section p {{
        font-size: 1rem !important;
        color: white !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}

    .q-card {{
        background-color: #FFFFFF; padding: 20px; border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #EAECEF; margin-top: 15px;
    }}
    
    .q-title {{ font-weight: 800; font-size: 1rem; color: #004A7C; margin-bottom: 5px; }}

    div[data-baseweb="radio"] {{
        background-color: #F5F5DC !important;
        padding: 10px 15px;
        border-radius: 12px;
        margin-bottom: 3px;
    }}

    .motto-box {{
        background-color: #F0F4F8;
        padding: 15px;
        border-radius: 15px;
        text-align: center;
        font-weight: 800;
        font-size: 1.2rem;
        color: #004A7C;
        margin-bottom: 20px;
        border: 1.5px solid #D1D9E0;
    }}

    .bio-card {{
        background-color: white; padding: 30px; border-radius: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); border: 1px solid #F0F0F0;
    }}

    .section-header {{
        font-size: 1.1rem; font-weight: 700; color: #004A7C;
        margin-top: 25px; margin-bottom: 10px; border-left: 5px solid #F5F5DC; padding-left: 12px;
    }}

    .stButton>button {{
        width: 100%; 
        border-radius: 18px !important; 
        border: 1.5px solid #331f00 !important; 
        background-color: #ffffff !important; 
        color: #004A7C !important;
        height: 3.5rem;
        font-weight: 700; 
        box-shadow: 0 8px 15px rgba(0,74,124,0.1);
    }}
</style>
""", unsafe_allow_html=True)

# --- 2. 데이터 정의 ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'survey_step' not in st.session_state: st.session_state.survey_step = 1
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'final_results' not in st.session_state: st.session_state.final_results = None
if 'selected_leader' not in st.session_state: st.session_state.selected_leader = 'Pioneer'

leaders_info = {
    "Pioneer": {
        "name": "정주영 (현대그룹 회장)", 
        "motto": "“이봐, 해봤어?”",
        "bio": "강원도 통천의 가난한 농가에서 태어난 그는 소 판 돈을 들고 무작정 상경하여 막노동부터 시작했습니다. 이후 쌀가게인 '경일상회'를 거쳐 현대자동차공업사와 현대건설을 설립하며 현대그룹의 기틀을 닦았습니다. 한국 전쟁 이후 폐허가 된 국토를 재건하고, 경부고속도로 건설과 조선소 건립 등 남들이 불가능하다고 했던 대형 프로젝트를 특유의 '현장 중심 실행력'으로 완수하며 대한민국 산업화의 상징이 되었습니다.",
        "case": "서산 간척지 공사 당시 빠른 물살로 인해 마지막 물막이가 어렵게 되자 고철로 매각될 예정이었던 거대 유조선을 침몰시켜 물길을 막는 기발한 공법을 창안했습니다. 또한 거북선이 그려진 500원권 지폐 한 장으로 영국 은행가들을 설득해 조선소 건립을 위한 차관을 따낸 일화는 전설적인 실행력의 사례로 꼽힙니다.",
        "hashtags": "#실행력 #현장주의 #불굴의투지 #창의적공법", "img": "images/jung.jpg"
    },
    "Architect": {
        "name": "이병철 (삼성그룹 회장)", 
        "motto": "“인재제일(人才第一), 사업보국(事業報國).”",
        "bio": "경남 의령의 유복한 가정에서 태어나 일본 유학을 다녀온 지식인이었습니다. 삼성상회를 시작으로 제일제당, 제일모직 등을 설립하며 수입 대체 산업을 일으켰습니다. '기업은 곧 사람'이라는 철학으로 한국 최초의 공채 제도를 도입하고 삼성전자를 설립하여 반도체 산업에 진출했습니다. 철저한 분석과 시스템을 중시하는 경영 스타일로 삼성을 세계적인 기술 기업으로 도약시키는 기반을 마련했습니다.",
        "case": "1983년 73세의 고령임에도 불구하고 미래 먹거리로 반도체를 점찍고 '도쿄 선언'을 통해 반도체 산업 진출을 선포했습니다. 주변의 극심한 반대와 회의적인 시각에도 불구하고 치밀한 준비와 과감한 투자 시스템을 가동하여 현재 삼성 반도체 신화의 초석을 다졌습니다.",
        "hashtags": "#전략가 #시스템경영 #인재육성 #선견지명", "img": "images/lee.jpg"
    },
    "Harmonizer": {
        "name": "구인회 (LG그룹 회장)", 
        "motto": "“한 번 믿으면 끝까지 믿는다.”",
        "bio": "경남 진주의 유교적 가풍에서 자라 화합과 신의를 무엇보다 소중히 여겼습니다. 락희화학공업(현 LG화학)과 금성사(현 LG전자)를 설립하며 한국의 화학 및 가전 산업을 개척했습니다. 특히 허씨 가문과의 수십 년간에 걸친 동업을 잡음 하나 없이 성공적으로 이끈 것으로 유명합니다. '인화(人和)'를 경영 이념으로 내세워 구성원들 간의 화합과 신뢰를 바탕으로 안정적인 성장을 추구했습니다.",
        "case": "기술도 자본도 없던 시절 모두가 수입에만 의존하던 라디오를 우리 기술로 만들겠다고 결심했습니다. 주변의 회의론 속에서도 기술자들을 끝까지 믿고 지원한 결과 한국 최초의 국산 라디오 'A-501'을 생산하는 데 성공했으며 이는 오늘날 가전 강국 대한민국의 시작점이 되었습니다.",
        "hashtags": "#인화경영 #상생 #신의 #가전개척자", "img": "images/koo.jpg"
    },
    "Steward": {
        "name": "박태준 (포스코 명예회장)", 
        "motto": "“짧은 인생을 영원한 조국에.”",
        "bio": "군인 출신으로 철저한 사명감과 국가관을 지닌 리더였습니다. '제철보국(철을 만들어 나라에 보답한다)'이라는 일념으로 황량한 영일만 모래벌판에 포항제철(현 포스코)을 세웠습니다. 정치적 풍랑 속에서도 오직 제철소 건설이라는 대의를 위해 외압을 막아내며 세계 최고의 경쟁력을 갖춘 제철소를 일궈냈습니다. 평생을 청렴하고 강직하게 살며 공적인 헌신의 표상이 되었습니다.",
        "case": "포항제철 건설 중 발전설비 송풍 시설에서 부실이 발견되자 완공을 앞둔 구조물을 가차 없이 폭파하고 재시공하게 했습니다. '적당히'라는 타협을 거부하고 세계 최고의 품질을 확보하려는 그의 완벽주의 정신은 포스코가 세계 1위 제철소가 되는 강력한 조직 문화를 만들었습니다.",
        "hashtags": ["#사명감", "#청렴강직", "#완벽주의", "#제철보국"], "img": "images/park.jpg"
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
    {"q": "11. 회의를 진행할 때 당신의 스타일은?", "a": "의견을 먼저 제시하고 동참을 구한다", "b": "전문가 보고를 듣고 최적안을 선택한다", "c": "편한 분위에서 경청한다", "d": "절차를 명확히 하고 결론에 집중한다"},
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

def go_to(page):
    st.session_state.page = page
    st.rerun()

def display_leader_image(img_path):
    if os.path.exists(img_path):
        st.image(Image.open(img_path), use_container_width=True)
    else:
        st.info("📷 인물 사진 업로드 대기 중")

# --- 4. 메인 렌더링 ---
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section"><h1>K-Leadership</h1><p>역사를 만든 거인들의 리더십 인사이트</p></div>', unsafe_allow_html=True)
    st.write("<br>"*2, unsafe_allow_html=True)
    if st.button("🔍 1. 리더십 성향 테스트 (START)"): 
        st.session_state.survey_step = 1
        go_to('survey')
    if st.button("📚 2. 리더십 대백과사전"): go_to('dictionary')

elif st.session_state.page == 'survey':
    step = st.session_state.survey_step
    st.markdown(f"### 📋 설문조사 ({step}/4)")
    st.progress(step * 0.25)
    start_idx = (step - 1) * 5
    for i in range(start_idx, start_idx + 5):
        st.markdown(f'<div class="q-card"><div class="q-title">QUESTION {i+1}</div>{questions[i]["q"]}</div>', unsafe_allow_html=True)
        st.session_state.answers[i] = st.radio("선택", [questions[i]['a'], questions[i]['b'], questions[i]['c'], questions[i]['d']], key=f"q{i}", label_visibility="collapsed")
    
    st.write("<br>", unsafe_allow_html=True)
    if step < 4:
        if st.button("다음 ➡️"): 
            st.session_state.survey_step += 1
            st.rerun()
    else:
        if st.button("최종 결과 확인하기 🏆"):
            s = {"Pioneer":0, "Architect":0, "Harmonizer":0, "Steward":0}
            for j in range(20):
                ans = st.session_state.answers.get(j)
                if ans == questions[j]['a']: s["Pioneer"]+=1
                elif ans == questions[j]['b']: s["Architect"]+=1
                elif ans == questions[j]['c']: s["Harmonizer"]+=1
                elif ans == questions[j]['d']: s["Steward"]+=1
            st.session_state.final_results = s
            go_to('result')
    if st.button("홈으로"): 
        go_to('home')

# [추가된 섹션] 결과 화면
elif st.session_state.page == 'result':
    st.header("🏆 당신의 리더십 모델")
    res = st.session_state.final_results
    if res:
        res_type = max(res, key=res.get)
        leader = leaders_info[res_type]
        
        st.markdown(f'<div class="motto-box">나의 리더십 모델: {leader["name"]}</div>', unsafe_allow_html=True)
        display_leader_image(leader['img'])
        st.markdown(f'<div class="bio-card"><p>{leader["bio"]}</p></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=go.Scatterpolar(r=[res['Pioneer'], res['Architect'], res['Harmonizer'], res['Steward']], theta=['개척', '설계', '화합', '원칙'], fill='toself', line=dict(color='#004A7C')))
        fig.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 10])), showlegend=False)
        st.plotly_chart(fig, config={'staticPlot': True}, use_container_width=True)
    
    if st.button("홈으로 돌아가기"): go_to('home')

# --- [수정] 2단계로 나뉜 인물 사전 로직 ---

# 1단계: 인물 목록 선택 화면
elif st.session_state.page == 'dictionary':
    st.header("📚 리더십 대백과사전")
    st.write("알고 싶은 리더를 선택해주세요.")
    
    st.markdown("""
        <style>
        .stButton>button {
            width: 100% !important;
            height: 3.2rem !important;
            font-size: 1.1rem !important;
            font-weight: 800 !important;
            border-radius: 15px !important;
            margin-bottom: 10px !important;
            border: 1.5px solid #004A7C !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2x2 그리드로 인물 선택 버튼 배치
    col1, col2 = st.columns(2)
    with col1:
        if st.button("정주영"):
            st.session_state.selected_leader = 'Pioneer'
            go_to('leader_detail')
        if st.button("구인회"):
            st.session_state.selected_leader = 'Harmonizer'
            go_to('leader_detail')
    with col2:
        if st.button("이병철"):
            st.session_state.selected_leader = 'Architect'
            go_to('leader_detail')
        if st.button("박태준"):
            st.session_state.selected_leader = 'Steward'
            go_to('leader_detail')
    
    st.write("<br>", unsafe_allow_html=True)
    if st.button("⬅️ 홈으로 돌아가기"):
        go_to('home')

# 2단계: 선택한 리더의 상세 정보 화면
elif st.session_state.page == 'leader_detail':
    info = leaders_info[st.session_state.selected_leader]
    
    st.header(f"📖 {info['name']}")
    
    # 좌우명 박스
    st.markdown(f'<div class="motto-box">{info["motto"]}</div>', unsafe_allow_html=True)
    
    # 상세 정보 카드 (사진 + 내용)
    st.markdown('<div class="bio-card">', unsafe_allow_html=True)
    display_leader_image(info['img'])
    
    st.markdown(f'<div class="section-header">📍 1. 그의 생애</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="line-height:1.7; margin-bottom:20px;">{info["bio"]}</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">💡 2. 리더십 성공 사례</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="line-height:1.7; margin-bottom:20px;">{info["case"]}</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">🏷️ 3. 리더십 키워드</div>', unsafe_allow_html=True)
    hashtags = info["hashtags"]
    if isinstance(hashtags, list): hashtags = " ".join(hashtags)
    st.markdown(f'<p style="font-weight:700; color:#555;">{hashtags}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    
    # 하단 내비게이션 버튼
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ 목록으로"):
            go_to('dictionary')
    with c2:
        if st.button("🏠 홈으로"):
            go_to('home')
