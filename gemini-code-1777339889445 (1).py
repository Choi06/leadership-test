import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os
import base64

# --- [1. 유틸리티 함수] ---

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

def go_to(page):
    st.session_state.page = page
    st.rerun()

def draw_value_chart(scores, name, color='#FF4B4B'):
    # 4대 가치(개척, 설계, 화합, 원칙) 사각형 지표
    categories = ['개척(A)', '설계(B)', '화합(C)', '원칙(D)']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor=color,
        line=dict(color=color),
        opacity=0.5
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        height=350,
        margin=dict(t=50, b=50, l=50, r=50),
        title=dict(text=f"<b>{name}</b>", x=0.5, font=dict(size=18, color='#004A7C'))
    )
    return fig

def display_leader_image(img_path):
    if os.path.exists(img_path):
        st.image(Image.open(img_path), use_container_width=True)
    else:
        st.info("📷 리더의 사진이 images 폴더에 없습니다.")

# --- [2. 앱 스타일 및 보안 설정] ---
st.set_page_config(page_title="K-Leadership Insight", layout="centered")

# 깃허브 아이콘 및 메뉴 숨기기
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

# 배경 이미지 설정
hero_img_path = "images/main_hero.jpg"
bin_str = get_base64_of_bin_file(hero_img_path)
hero_bg_style = f"url('data:image/jpg;base64,{bin_str}')" if bin_str else "linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5))"

# 전역 디자인 (둥근 카드 + 버튼 색상 고정)
st.markdown(f"""
<link rel="stylesheet" as="style" crossorigin href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css" />
<style>
    html, body, [class*="st-"] {{ font-family: 'Pretendard', sans-serif; color: #1A1A1A !important; }}
    .stApp {{ background-color: #F8F9FB; }}
    
    .hero-section {{
        background-image: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), {hero_bg_style};
        background-size: cover; background-position: center; height: 220px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        border-radius: 25px; margin-bottom: 20px; color: white !important; text-align: center;
    }}

    .q-card {{
        background-color: #FFFFFF; padding: 25px; border-radius: 20px;
        border: 1px solid #EAECEF; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }}
    .q-title {{ font-weight: 800; font-size: 0.85rem; color: #004A7C; opacity: 0.6; }}
    .q-text {{ font-size: 1.1rem; font-weight: 700; margin-top: 5px; }}

    div[data-baseweb="radio"] {{
        background-color: #F5F5DC !important; padding: 12px 20px !important;
        border-radius: 12px !important; margin-bottom: 8px !important;
        border: 1px solid #EAECEF !important;
    }}
    div[data-baseweb="radio"] label p {{ color: #004A7C !important; font-weight: 600 !important; }}

    .stButton>button {{
        width: 100% !important; border-radius: 15px !important;
        background-color: #FFFFFF !important; color: #004A7C !important;
        height: 3.5rem !important; font-weight: 700 !important;
        border: 1.5px solid #004A7C !important;
    }}
    .stButton>button:hover {{ background-color: #004A7C !important; color: #FFFFFF !important; }}

    .summary-box {{ 
        background-color: #F0F4F8; padding: 20px; border-radius: 15px; 
        text-align: center; font-weight: 800; font-size: 1.3rem; color: #004A7C; 
        border: 1.5px solid #D1D9E0; margin-bottom: 25px;
    }}
</style>
""", unsafe_allow_html=True)

# --- 2. 데이터 정의 (내용 보강 버전) ---
if 'page' not in st.session_state: st.session_state.page = 'home'
if 'survey_step' not in st.session_state: st.session_state.survey_step = 1
if 'answers' not in st.session_state: st.session_state.answers = {}
    
leaders_info = {
    "Pioneer": {
        "name": "정주영 (현대그룹 회장)",
        "motto": "“이봐, 해봤어?”",
        "scores": [10, 7, 7, 8, 9], 
        "timeline": [
            ("1915", "강원도 통천 가난한 농가 6남 2녀 중 장남으로 출생"),
            ("1946", "현대자동차공업사 설립 (현대그룹의 모태)"),
            ("1970", "세계 최단기간 완공 기록인 경부고속도로 준공"),
            ("1984", "서산 간척지 A지구 물막이 공사 '유조선 공법' 성공"),
            ("1998", "소 500마리와 함께 판문점을 통과해 방북 (소떼 방북)"),
            ("2001", "타계 (대한민국 산업화의 불굴의 상징)")
        ],
        "bio": """가난한 농부의 아들로 태어나 가출을 반복하며 막노동, 쌀가게 배달원 등으로 사회생활을 시작했습니다. 
        그의 생애는 '시련은 있어도 실패는 없다'는 그의 자서전 제목처럼, 불가능해 보이는 과업을 특유의 배짱과 현장 감각으로 돌파한 역사입니다. 
        단순한 기업인을 넘어 전후 폐허가 된 대한민국에 도로를 깔고, 배를 만들고, 자동차를 수출하며 '우리도 할 수 있다'는 국민적 자신감을 심어준 개척자입니다. 
        이론보다는 현장을, 책상보다는 작업복을 사랑했던 그는 한국 현대 경제사의 살아있는 신화로 평가받습니다.""",
        "case": """[서산 간척지 유조선 공법] 1984년, 충남 서산 간척지 공사 중 초당 8m의 거센 물살 때문에 마지막 물막이 공사가 한계에 부딪혔습니다. 
        현대건설 기술진도 포기하려던 순간, 그는 고철로 매각될 예정이었던 23만 톤급 폐유조선을 끌어와 물길을 막는 기상천외한 아이디어를 냈습니다. 
        전 세계 토목 역사에 유례가 없던 이 '아산 공법'은 공사 기간을 9개월 단축하고 280억 원의 비용을 절감했습니다. 
        이는 지식의 한계를 창의적 실행력으로 극복한 리더십의 정수로 꼽힙니다.""",
        "hashtags": "#실행력 #현장주의 #불굴의투지 #창의적공법",
        "img": "images/jung.jpg"
    },
    "Architect": {
        "name": "이병철 (삼성그룹 회장)",
        "motto": "“인재제일(人才第一), 사업보국(事業報國).”",
        "scores": [8, 10, 8, 9, 8],
        "timeline": [
            ("1910", "경남 의령 유복한 가문의 막내로 출생"),
            ("1938", "대구에서 삼성상회 설립 (수출업 시작)"),
            ("1953", "제일제당 설립으로 수입 대체 산업화 주도"),
            ("1969", "삼성전자공업 설립"),
            ("1983", "2월 8일, 도쿄 선언을 통해 반도체 본격 진출 선포"),
            ("1987", "타계 (글로벌 삼성의 기반을 닦은 전략가)")
        ],
        "bio": """일본 와세다 대학에서 수학하며 근대적 경영 감각을 익힌 지식인 경영자였습니다. 
        그는 '사업보국(사업을 통해 나라를 이롭게 한다)'을 평생의 신념으로 삼아, 설탕, 옷감부터 전자제품까지 국민 생활에 필수적인 산업을 단계적으로 일으켰습니다. 
        특히 '의심나면 쓰지 말고, 썼으면 의심하지 말라'는 용인술로 한국 최초의 공채 제도를 도입하는 등 시스템 중심의 경영 문화를 정착시켰습니다. 
        삼성이 오늘날 글로벌 1위 기업이 된 배경에는 그의 철저한 분석력과 완벽주의가 깔린 '관리의 삼성' 시스템이 있습니다.""",
        "case": """[2.8 도쿄 선언과 반도체 신화] 1983년, 73세의 고령이었던 그는 '반도체가 나라의 미래를 결정한다'는 확신으로 반도체 사업 진출을 선포했습니다. 
        당시 인텔과 같은 세계적 기업들도 무모하다고 비웃었으나, 그는 6개월 만에 64K D램 개발에 성공하며 세계를 경악하게 했습니다. 
        이는 단순한 투자가 아니라 10년 뒤를 내다본 리더의 선견지명과, 한 번 정한 목표는 끝까지 완수하는 치밀한 전략적 리더십이 만들어낸 대한민국 경제의 최대 변곡점이었습니다.""",
        "hashtags": "#전략가 #시스템경영 #인재육성 #선견지명",
        "img": "images/lee.jpg"
    },
    "Harmonizer": {
        "name": "구인회 (LG그룹 회장)",
        "motto": "“한 번 믿으면 끝까지 믿는다.”",
        "scores": [7, 8, 10, 8, 8],
        "timeline": [
            ("1907", "경남 진주의 유교 가풍 가문에서 장남으로 출생"),
            ("1947", "락희화학공업 설립 (한국 화학 산업의 효시)"),
            ("1958", "금성사 설립 (한국 가전 산업의 개척)"),
            ("1959", "대한민국 최초의 국산 라디오 'A-501' 생산"),
            ("1966", "국내 최초의 흑백 텔레비전 생산"),
            ("1969", "타계 (LG 인화 경영의 뿌리)")
        ],
        "bio": """'남들이 하지 않는 것을 먼저 하여 국가에 도움이 되어야 한다'는 철학으로 한국 화학과 가전 산업을 동시에 일구었습니다. 
        그의 리더십은 '인화(人和)'로 요약됩니다. 특히 허씨 가문과의 57년에 걸친 동업 과정에서 단 한 번의 잡음도 없었던 것은 신의를 목숨처럼 여긴 그의 인품 덕분이었습니다. 
        직원들을 가족처럼 아끼며 '사람이 재산이다'라는 믿음을 실천했고, 이는 오늘날 LG그룹이 고객의 신뢰를 중시하는 기업 문화를 갖게 된 근간이 되었습니다.""",
        "case": """[최초의 국산 라디오 개발] 1950년대 말, 외제 라디오가 주류를 이루던 시절 그는 '우리 기술로 우리말을 듣게 하겠다'는 결심으로 라디오 국산화에 착수했습니다. 
        기술진들이 실패를 반복할 때도 "실패를 두려워하면 발전이 없다"며 끝까지 격려하고 자금을 지원했습니다. 
        결국 1959년 탄생한 국산 라디오 'A-501'은 한국 전자 산업의 시작점이 되었으며, 기술자들의 자긍심을 고취시킨 그의 '기다림과 믿음의 리더십'은 가전 강국 대한민국의 씨앗이 되었습니다.""",
        "hashtags": "#인화경영 #상생 #신의 #가전개척자",
        "img": "images/koo.jpg"
    },
    "Steward": {
        "name": "박태준 (포스코 명예회장)",
        "motto": "“짧은 인생을 영원한 조국에.”",
        "scores": [9, 8, 7, 10, 7],
        "timeline": [
            ("1927", "경남 양산 출생 및 와세다 대학 수학"),
            ("1968", "포항종합제철 사장 취임 (모래벌판에서 시작)"),
            ("1973", "대한민국 현대사 최초의 쇳물 생산"),
            ("1986", "포항공과대학교(POSTECH) 설립"),
            ("1992", "세계 최고 수준의 포항/광양 제철소 완공"),
            ("2011", "타계 (청렴한 영웅으로 남음)")
        ],
        "bio": """'제철보국(철을 만들어 나라에 보답한다)'이라는 사명감 하나로 평생을 바친 리더입니다. 
        포항의 모래벌판에서 제철소 건설을 시작할 때, 조상들의 피값(대일청구권 자금)으로 짓는 것인 만큼 '실패하면 우향우해서 영일만 바다에 빠져 죽자'는 비장한 각오로 임했습니다. 
        그는 정치적 풍랑 속에서도 오직 제철소라는 대의를 위해 외압을 막아낸 방파제였으며, 퇴임 시 주식 한 주도 갖지 않고 청렴하게 삶을 마무리하여 공직자와 리더의 표상이 되었습니다.""",
        "case": """[부실공사 폭파 사건] 1977년, 포항제철 3기 설비 공사 중 발전 송풍 시설의 기초 콘크리트에서 미세한 부실이 발견되었습니다. 
        이미 80% 이상 완공되어 막대한 비용이 투입된 상태였으나, 그는 "부실의 싹은 아예 없어야 한다"며 구조물을 가차 없이 폭파시켰습니다. 
        이 충격적인 조치는 전 직원에게 '적당히'라는 타협을 버리게 했고, 포스코가 세계 최고의 품질 경쟁력을 갖춘 1위 제철소가 되는 결정적 계기가 되었습니다. 원칙과 타협하지 않는 그의 무결점 경영 철학을 보여주는 유명한 일화입니다.""",
        "hashtags": "#사명감 #청렴강직 #완벽주의 #제철보국",
        "img": "images/park.jpg"
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

# --- 3. 메인 로직 제어 ---

# --- [4. 페이지 렌더링 로직] ---

# [HOME]
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section"><h1>K-Leadership</h1><p>역사를 만든 거인들의 인사이트</p></div>', unsafe_allow_html=True)
    if st.button("🔍 성향 테스트 시작"): 
        st.session_state.survey_step = 1
        go_to('survey')
    if st.button("📚 리더십 대백과사전"): go_to('dictionary')

# [SURVEY]
elif st.session_state.page == 'survey':
    step = st.session_state.survey_step
    st.markdown(f"### 📋 설문 진행 ({step}/4)")
    st.progress(step * 0.25)
    
    start_idx = (step - 1) * 5
    for i in range(start_idx, start_idx + 5):
        st.markdown(f'''<div class="q-card">
            <div class="q-title">QUESTION {i+1}</div>
            <div class="q-text">{questions[i]["q"]}</div>
        </div>''', unsafe_allow_html=True)
        st.session_state.answers[i] = st.radio(f"q{i}", 
            [questions[i]['a'], questions[i]['b'], questions[i]['c'], questions[i]['d']], 
            key=f"r_{i}", label_visibility="collapsed")
    
    st.write("<br>", unsafe_allow_html=True)
    c_p, c_n = st.columns(2)
    with c_p:
        if step > 1:
            if st.button("⬅️ 이전"): st.session_state.survey_step -= 1; st.rerun()
        else:
            if st.button("🏠 홈으로"): go_to('home')
    with c_n:
        if step < 4:
            if st.button("다음 ➡️"): st.session_state.survey_step += 1; st.rerun()
        else:
            if st.button("결과 확인 🏆"): go_to('result')

# [RESULT - 리더 사진 + 나의 사각형 지표 배치]
elif st.session_state.page == 'result':
    st.header("🏆 리더십 분석 결과")
    
    # 1. 유사도 기반 인물 매칭
    counts = {"Pioneer": 0, "Architect": 0, "Harmonizer": 0, "Steward": 0}
    for i in range(20):
        ans = st.session_state.answers.get(i)
        if ans == questions[i]['a']: counts["Pioneer"] += 1
        elif ans == questions[i]['b']: counts["Architect"] += 1
        elif ans == questions[i]['c']: counts["Harmonizer"] += 1
        elif ans == questions[i]['d']: counts["Steward"] += 1
    
    res_type = max(counts, key=counts.get)
    leader = leaders_info[res_type]
    
    # 2. 나의 가치 지표 점수 환산
    user_values = [counts["Pioneer"]*2, counts["Architect"]*2, counts["Harmonizer"]*2, counts["Steward"]*2]

    st.markdown(f'<div class="summary-box">당신은 <b>{leader["name"]}</b> 스타일의 리더입니다!</div>', unsafe_allow_html=True)
    
    # 3. [핵심] 리더 사진과 나의 지표 차트 좌우 배치
    col_img, col_chart = st.columns([1, 1.2]) # 사진과 차트 비율
    
    with col_img:
        st.markdown("**매칭된 리더십 인물**")
        display_leader_image(leader['img'])
        st.markdown(f"<div style='text-align:center; font-weight:700; color:#004A7C;'>{leader['name']}</div>", unsafe_allow_html=True)
        
    with col_chart:
        # 나의 4대 가치 평가 척도 그래프
        st.plotly_chart(draw_value_chart(user_values, "나의 리더십 가치 사각형"), use_container_width=True)
    
    # 4. 상세 설명 카드
    st.markdown(f'''
        <div class="q-card">
            <p style="font-size:1.1rem; line-height:1.7;">
                <b>성향 분석:</b><br>{leader["bio"]}
            </p>
            <hr>
            <p style="font-size:1.1rem; line-height:1.7;">
                <b>성공 사례로 보는 인사이트:</b><br>{leader["case"]}
            </p>
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button("🏠 홈으로 돌아가기"): go_to('home')
