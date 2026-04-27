import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- 페이지 설정 및 디자인 ---
st.set_page_config(page_title="K-리더십 인사이트", layout="wide")

# UI 커스텀 스타일링
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #004a7c; color: white; }
    .leader-card {
        background-color: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
        border-left: 5px solid #004a7c;
    }
    .motto { font-style: italic; color: #555; font-size: 1.1em; margin-bottom: 10px; }
    .hashtag { color: #007bff; font-weight: bold; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 데이터 정의 ---
leaders_info = {
    "Pioneer": {
        "name": "정주영 (현대그룹 창업주)",
        "motto": "“시련은 있어도 실패는 없다.”",
        "bio": "강원도 통천의 가난한 농군으로 태어나 현대그룹을 일궈낸 '한국 경제의 거인'.",
        "case": "서산 간척지 공사 당시 대형 유조선으로 물막이를 하는 '정주영 공법'으로 세계를 놀라게 함.",
        "hashtags": ["#실행력", "#불도저", "#현장중심", "#무한도전"],
        "color": "#005aab"
    },
    "Architect": {
        "name": "이병철 (삼성그룹 창업주)",
        "motto": "“인재제일(人才第一), 사업보국(事業報國).”",
        "bio": "치밀한 분석과 선견지명으로 삼성을 글로벌 기업의 반열에 올린 '전략적 설계자'.",
        "case": "1983년 73세의 나이에 주위의 반대를 무릅쓰고 반도체 투자를 결정, 오늘날 IT 강국의 기틀을 닦음.",
        "hashtags": ["#시스템", "#데이터", "#선견지명", "#합리주의"],
        "color": "#0047a0"
    },
    "Harmonizer": {
        "name": "구인회 (LG그룹 창업주)",
        "motto": "“한 번 사람을 믿으면 끝까지 믿는다. 인화(人和)가 제일이다.”",
        "bio": "상생과 화합을 바탕으로 LG를 '신뢰의 기업'으로 키워낸 포용적 리더.",
        "case": "동업자와의 갈등 없이 수십 년간 파트너십을 유지하며, 화학과 전자 산업의 불모지에서 성공을 일궈냄.",
        "hashtags": ["#인화", "#상생", "#신뢰경영", "#포용적리더"],
        "color": "#a50034"
    },
    "Steward": {
        "name": "박태준 (포스코 명예회장)",
        "motto": "“짧은 인생을 영원한 조국에. 제철보국(製鐵報國).”",
        "bio": "무에서 유를 창조하며 한국 철강 산업의 신화를 쓴 '강직한 사명가'.",
        "case": "포항제철 건설 당시 부실 공사가 발견되자 다 지어진 구조물을 폭파하며 '무결점 완벽주의'를 실천함.",
        "hashtags": ["#사명감", "#무결점", "#원칙주의", "#정면돌파"],
        "color": "#434b54"
    }
}

# --- 앱 로직 ---
st.sidebar.title("🇰🇷 K-Leadership Index")
choice = st.sidebar.radio("원하시는 메뉴를 선택하세요:", ["1. 나의 리더십 모델 찾아보기", "2. 한국의 리더십 모델 알아보기"])

# --- 1번 메뉴: 리더십 검사 ---
if choice == "1. 나의 리더십 모델 찾아보기":
    st.header("🔍 나의 리더십 유형 검사")
    st.write("20개의 문항을 통해 당신의 잠재적 리더십 스타일을 분석합니다.")
    st.markdown("---")

    # 20개 문항 데이터 (이전과 동일하지만 UI 개선)
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

    with st.form("survey_form"):
        user_answers = []
        for i, q in enumerate(questions):
            ans = st.radio(q['q'], [q['a'], q['b'], q['c'], q['d']], key=f"q{i}")
            user_answers.append(ans)
        
        submitted = st.form_submit_button("나의 리더십 결과 보기")

        if submitted:
            # 점수 계산
            scores = {"Pioneer": 0, "Architect": 0, "Harmonizer": 0, "Steward": 0}
            for i, ans in enumerate(user_answers):
                if ans == questions[i]['a']: scores["Pioneer"] += 1
                elif ans == questions[i]['b']: scores["Architect"] += 1
                elif ans == questions[i]['c']: scores["Harmonizer"] += 1
                elif ans == questions[i]['d']: scores["Steward"] += 1
            
            res_type = max(scores, key=scores.get)
            leader_match = leaders_info[res_type]
            
            st.balloons()
            st.markdown("---")
            st.subheader(f"축하합니다! 당신은 **[{leader_match['name']}]** 스타일입니다.")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(f"### {leader_match['motto']}")
                st.write(leader_match['bio'])
                tags = " ".join([f"<span class='hashtag'>{tag}</span>" for tag in leader_match['hashtags']])
                st.markdown(tags, unsafe_allow_html=True)
            
            with col2:
                # 레이더 차트
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=[scores['Pioneer'], scores['Architect'], scores['Harmonizer'], scores['Steward']],
                    theta=['정주영(개척)', '이병철(설계)', '구인회(화합)', '박태준(원칙)'],
                    fill='toself', fillcolor='rgba(0, 74, 124, 0.5)', line=dict(color='#004a7c')
                ))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 20])), showlegend=False)
                st.plotly_chart(fig)

# --- 2번 메뉴: 리더십 사전 ---
else:
    st.header("📚 한국형 리더십 사전")
    st.write("대한민국 경제 성장을 이끈 핵심 리더 4인의 철학과 사례를 정리했습니다.")
    st.markdown("---")

    # 4인 인물 섹터 구분
    for key, info in leaders_info.items():
        st.markdown(f"""
        <div class="leader-card">
            <h2>{info['name']}</h2>
            <p class="motto">{info['motto']}</p>
            <hr>
            <p><strong>📍 약력:</strong> {info['bio']}</p>
            <p><strong>💡 리더십 사례:</strong> {info['case']}</p>
            <p><strong>🏷️ 키워드:</strong> {' '.join([f'<span class="hashtag">{t}</span>' for t in info['hashtags']])}</p>
        </div>
        """, unsafe_allow_html=True)