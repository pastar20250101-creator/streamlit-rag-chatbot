# ============================================================
# 💗 썸 시그널 분석기
# 실행: streamlit run final_project_starter.py
# ============================================================

import time
import random
import pandas as pd
import streamlit as st


# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="썸 시그널 분석기",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 디자인 CSS
# ============================================================
st.markdown(
    """
    <style>
    /* -------------------------------------------------------
       전체 색상 및 기본 디자인
    ------------------------------------------------------- */
    :root {
        --pink-main: #e96f9d;
        --pink-dark: #b84772;
        --pink-soft: #fff1f6;
        --pink-pale: #fff8fb;
        --rose-border: #f5d7e3;
        --lavender: #f5f0ff;
        --text-main: #3c3036;
        --text-sub: #7e6a73;
    }

    .stApp {
        background:
            radial-gradient(circle at 5% 5%, #fff1f7 0, transparent 28%),
            radial-gradient(circle at 95% 15%, #f8f2ff 0, transparent 24%),
            linear-gradient(180deg, #fffdfd 0%, #fff8fb 100%);
    }

    html, body, [class*="css"] {
        color: var(--text-main);
    }

    /* -------------------------------------------------------
       상단 제목 영역
    ------------------------------------------------------- */
    .hero {
        text-align: center;
        padding: 24px 20px 16px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 15px;
        border-radius: 999px;
        background: #fff0f5;
        border: 1px solid #f4cedd;
        color: #b84772;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: clamp(34px, 5vw, 52px);
        font-weight: 850;
        letter-spacing: -0.05em;
        color: #3c3036;
        margin-bottom: 8px;
    }

    .hero-title span {
        color: #d95d8d;
    }

    .hero-description {
        max-width: 680px;
        margin: 0 auto;
        color: #806c75;
        font-size: 16px;
        line-height: 1.75;
    }

    /* -------------------------------------------------------
       카드
    ------------------------------------------------------- */
    .love-card {
        background: rgba(255, 255, 255, 0.86);
        border: 1px solid #f2dbe4;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 14px 36px rgba(168, 79, 113, 0.07);
        margin-bottom: 18px;
    }

    .result-card {
        background:
            linear-gradient(
                135deg,
                rgba(255, 242, 247, 0.95),
                rgba(250, 246, 255, 0.95)
            );
        border: 1px solid #f0d5e1;
        border-radius: 24px;
        padding: 25px;
        margin-bottom: 20px;
    }

    .result-label {
        color: #b84772;
        font-size: 13px;
        font-weight: 750;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }

    .result-grade {
        font-size: 27px;
        font-weight: 850;
        letter-spacing: -0.04em;
        margin-bottom: 9px;
    }

    .result-summary {
        color: #74626a;
        line-height: 1.7;
        margin: 0;
    }

    /* -------------------------------------------------------
       점수 게이지
    ------------------------------------------------------- */
    .gauge-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 8px 0 20px;
    }

    .gauge {
        width: 190px;
        height: 190px;
        border-radius: 50%;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 16px 32px rgba(207, 85, 133, 0.13);
    }

    .gauge::before {
        content: "";
        position: absolute;
        width: 145px;
        height: 145px;
        background: #fffdfd;
        border-radius: 50%;
        box-shadow: inset 0 0 0 1px #fae8ef;
    }

    .gauge-content {
        position: relative;
        z-index: 2;
        text-align: center;
    }

    .gauge-score {
        font-size: 45px;
        font-weight: 900;
        line-height: 1;
        color: #c84e7d;
        letter-spacing: -0.06em;
    }

    .gauge-unit {
        margin-top: 7px;
        font-size: 14px;
        color: #8f737e;
        font-weight: 700;
    }

    /* -------------------------------------------------------
       시그널 칩
    ------------------------------------------------------- */
    .signal-chip {
        display: flex;
        gap: 10px;
        align-items: flex-start;
        padding: 13px 15px;
        border-radius: 15px;
        margin-bottom: 9px;
        line-height: 1.55;
        font-size: 14px;
    }

    .positive-chip {
        background: #fff0f5;
        border: 1px solid #f5d4e1;
        color: #684651;
    }

    .caution-chip {
        background: #fff8ef;
        border: 1px solid #f2e0c8;
        color: #6e5943;
    }

    .neutral-chip {
        background: #f7f3ff;
        border: 1px solid #e6dcf7;
        color: #5b506d;
    }

    /* -------------------------------------------------------
       추천 답장
    ------------------------------------------------------- */
    .reply-card {
        background: #fff;
        border: 1px solid #f0d4df;
        border-left: 5px solid #df6996;
        border-radius: 18px;
        padding: 20px;
        margin: 12px 0;
        color: #4b3840;
        font-size: 16px;
        line-height: 1.7;
    }

    .tip-card {
        background: #f7f2ff;
        border: 1px solid #e8ddf8;
        border-radius: 16px;
        padding: 16px 18px;
        color: #5f536c;
        margin-top: 12px;
    }

    /* -------------------------------------------------------
       Streamlit 기본 요소 수정
    ------------------------------------------------------- */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid #f1dae3;
        padding: 17px;
        border-radius: 18px;
        box-shadow: 0 8px 22px rgba(160, 80, 110, 0.05);
    }

    div[data-testid="stMetricValue"] {
        color: #c44f7c;
    }

    div[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #fff8fb 0%,
                #fdf7ff 100%
            );
        border-right: 1px solid #f2dce5;
    }

    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid #f2dde5;
        border-radius: 18px;
        padding: 8px;
        margin-bottom: 12px;
    }

    .stButton > button {
        border-radius: 14px;
        min-height: 44px;
        font-weight: 700;
        border: 1px solid #edcbd8;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #dc668f, #c84d7b);
        color: white;
        border: none;
        box-shadow: 0 8px 20px rgba(201, 76, 123, 0.18);
    }

    .stTextInput input,
    .stTextArea textarea,
    div[data-baseweb="select"] > div {
        border-radius: 14px;
    }

    button[data-baseweb="tab"] {
        font-weight: 700;
    }

    /* 외부 링크 버튼 숨김 */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 세션 상태 초기화
# ============================================================
def initialize_session_state():
    default_values = {
        "nickname": "",
        "messages": [],
        "score_history": [],
        "analysis_count": 0,
        "celebrated": False,
        "last_result": None,
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


initialize_session_state()


# ============================================================
# 메시지 분석
# ============================================================
def analyze_signal(message, relationship_stage):
    message = message.strip()
    lower_message = message.lower()

    score = 46

    positive_signals = []
    caution_signals = []

    category_scores = {
        "대화 지속성": 40,
        "관심 표현": 40,
        "정서적 온도": 45,
        "구체성": 40,
    }

    positive_keywords = {
        "보고 싶": 14,
        "또 보": 13,
        "다음에": 10,
        "같이": 7,
        "즐거웠": 10,
        "재밌었": 9,
        "좋았": 7,
        "궁금": 6,
        "뭐 해": 7,
        "잘 들어갔": 8,
        "조심히": 5,
        "연락해": 5,
        "기다릴": 8,
        "시간 돼": 10,
        "언제 시간": 11,
        "생각나": 11,
        "약속": 8,
        "맛있는": 5,
        "ㅋㅋ": 3,
        "ㅎㅎ": 3,
        "😊": 4,
        "🥰": 8,
        "😍": 7,
        "❤️": 8,
        "💕": 8,
    }

    caution_keywords = {
        "바빠": -7,
        "나중에": -4,
        "언젠가": -6,
        "글쎄": -7,
        "모르겠": -6,
        "피곤": -4,
        "연락할게": -3,
        "시간 되면": -5,
        "기회 되면": -6,
        "ㅇㅇ": -6,
        "넵": -3,
    }

    for keyword, value in positive_keywords.items():
        if keyword in lower_message:
            score += value
            positive_signals.append(
                f"‘{keyword}’ 표현에서 친근함이나 관심의 가능성이 보여요."
            )

            if keyword in ["다음에", "또 보", "시간 돼", "언제 시간", "약속"]:
                category_scores["대화 지속성"] += 18
                category_scores["관심 표현"] += 15

            elif keyword in ["보고 싶", "생각나", "궁금"]:
                category_scores["관심 표현"] += 22
                category_scores["정서적 온도"] += 15

            elif keyword in ["ㅋㅋ", "ㅎㅎ", "😊", "🥰", "😍", "❤️", "💕"]:
                category_scores["정서적 온도"] += 17

            else:
                category_scores["관심 표현"] += 9

    for keyword, value in caution_keywords.items():
        if keyword in lower_message:
            score += value
            caution_signals.append(
                f"‘{keyword}’ 표현은 상황에 따라 거리감으로 느껴질 수 있어요."
            )
            category_scores["관심 표현"] -= 8
            category_scores["대화 지속성"] -= 6

    # 질문 분석
    question_count = message.count("?") + message.count("？")

    if question_count > 0:
        score += 9
        category_scores["대화 지속성"] += 24
        category_scores["구체성"] += 8
        positive_signals.append(
            "질문이 포함되어 있어 대화를 이어가려는 흐름이 보여요."
        )
    else:
        caution_signals.append(
            "질문이 없어 현재 메시지만으로는 대화 지속 의도를 판단하기 어려워요."
        )

    # 길이 분석
    message_length = len(message)

    if message_length >= 45:
        score += 8
        category_scores["구체성"] += 28
        positive_signals.append(
            "메시지가 비교적 길고 구체적이어서 성의 있는 답장으로 볼 수 있어요."
        )

    elif message_length >= 20:
        score += 4
        category_scores["구체성"] += 17
        positive_signals.append(
            "메시지 길이가 적당하고 내용이 비교적 구체적이에요."
        )

    elif message_length <= 5:
        score -= 14
        category_scores["구체성"] -= 20
        category_scores["대화 지속성"] -= 12
        caution_signals.append(
            "답장이 매우 짧아 앞뒤 대화 맥락을 함께 확인해야 해요."
        )

    elif message_length <= 10:
        score -= 6
        category_scores["구체성"] -= 10
        caution_signals.append(
            "메시지가 짧은 편이라 단정하기에는 정보가 부족해요."
        )

    # 느낌표 분석
    if "!" in message:
        score += 3
        category_scores["정서적 온도"] += 8
        positive_signals.append(
            "느낌표가 포함되어 있어 비교적 밝은 감정 표현으로 보일 수 있어요."
        )

    # 관계 단계 보정
    stage_bonus = {
        "소개팅 전": -2,
        "소개팅 직후": 4,
        "연락 중": 2,
        "두 번째 만남 준비": 6,
    }

    score += stage_bonus.get(relationship_stage, 0)

    # 범위 제한
    score = max(0, min(score, 100))

    for category in category_scores:
        category_scores[category] = max(
            0,
            min(category_scores[category], 100),
        )

    positive_signals = list(dict.fromkeys(positive_signals))
    caution_signals = list(dict.fromkeys(caution_signals))

    if score >= 85:
        grade = "두근두근, 강한 관심 신호"
        summary = (
            "대화를 이어가려는 표현과 정서적인 친밀감이 함께 나타났어요. "
            "자연스럽게 다음 만남을 제안해 볼 수 있는 흐름입니다."
        )
        emoji = "💖"
        signal_level = "매우 긍정적"

    elif score >= 70:
        grade = "기분 좋은 호감 신호"
        summary = (
            "호감으로 해석할 수 있는 표현이 여러 개 보여요. "
            "상대방의 대화 속도와 분위기에 맞춰 천천히 이어가 보세요."
        )
        emoji = "💗"
        signal_level = "긍정적"

    elif score >= 55:
        grade = "은근한 관심 가능성"
        summary = (
            "긍정적인 요소가 있지만 아직 확실한 판단을 내리기에는 "
            "대화 정보가 조금 부족해요."
        )
        emoji = "💓"
        signal_level = "관찰 필요"

    elif score >= 40:
        grade = "조금 더 지켜볼 단계"
        summary = (
            "현재 메시지는 예의 있는 답장이나 일상적인 대화일 수 있어요. "
            "메시지 한 번보다 반복되는 행동을 살펴보세요."
        )
        emoji = "💬"
        signal_level = "중립"

    else:
        grade = "거리 조절이 필요한 신호"
        summary = (
            "현재 메시지만 보면 적극적인 관심은 크지 않을 수 있어요. "
            "답장을 재촉하거나 과도하게 의미를 부여하지 않는 편이 좋습니다."
        )
        emoji = "🩶"
        signal_level = "거리감 가능"

    return {
        "score": score,
        "grade": grade,
        "summary": summary,
        "emoji": emoji,
        "signal_level": signal_level,
        "positive_signals": positive_signals,
        "caution_signals": caution_signals,
        "category_scores": category_scores,
    }


# ============================================================
# 답장 추천
# ============================================================
def recommend_reply(tone, relationship_stage, result):
    replies = {
        "부담 없게": [
            "저도 즐거웠어요! 조심히 들어가셨죠? 다음에 또 편하게 봬요 😊",
            "오늘 좋은 시간이었어요. 남은 하루도 편안하게 보내세요!",
            "저도 즐거웠어요! 다음에 맛있는 거 먹으면서 또 이야기해요 😊",
        ],
        "다정하게": [
            "저도 오늘 정말 즐거웠어요 😊 덕분에 시간 가는 줄 몰랐네요. 조심히 들어가세요!",
            "오늘 만나서 정말 반가웠어요. 이야기 나누는 시간이 편하고 좋았어요 💗",
            "저도 즐거웠어요! 집에는 잘 들어가셨죠? 푹 쉬세요 😊",
        ],
        "유머러스하게": [
            "저도 즐거웠어요! 시간 순삭의 범인은 아무래도 우리였던 것 같네요 😆",
            "오늘 재미있었어요. 다음에는 더 맛있는 메뉴로 2차 면접 진행하시죠 😄",
            "대화가 너무 잘 통해서 시간 확인을 깜빡했네요 ㅋㅋ 다음에 또 봬요!",
        ],
        "적극적으로": [
            "저도 정말 즐거웠어요! 다음에 또 만나고 싶은데 이번 주말은 어떠세요? 😊",
            "오늘 이야기 나누는 시간이 좋았어요. 다음에는 제가 맛있는 곳 찾아볼게요!",
            "저도 즐거웠어요. 다음 만남은 제가 먼저 제안해도 될까요? 💗",
        ],
        "예의 바르게": [
            "저도 오늘 즐거운 시간이었습니다. 조심히 들어가시고 편안한 저녁 보내세요.",
            "오늘 만나 뵙게 되어 반가웠습니다. 좋은 시간 만들어 주셔서 감사합니다 😊",
            "저도 즐거웠습니다. 귀가길 조심하시고 다음에 또 뵙겠습니다.",
        ],
    }

    reply = random.choice(replies[tone])

    if result["score"] < 45 and tone == "적극적으로":
        reply = (
            "오늘 만나서 반가웠어요. 조심히 들어가시고 "
            "편안한 저녁 보내세요 😊"
        )

    tips = {
        "소개팅 전": (
            "약속 전에는 감정 표현보다 시간과 장소를 명확히 확인하는 것이 좋아요."
        ),
        "소개팅 직후": (
            "즐거웠다는 표현과 함께 귀가 여부를 묻는 답장이 자연스러워요."
        ),
        "연락 중": (
            "상대방의 답장 길이와 속도에 비슷한 텐션으로 맞춰보세요."
        ),
        "두 번째 만남 준비": (
            "날짜와 활동을 구체적으로 제안하면 관계가 더 자연스럽게 진전돼요."
        ),
    }

    return reply, tips[relationship_stage]


# ============================================================
# 게이지 HTML
# ============================================================
def render_signal_gauge(score):
    gauge_color = "#d95f8c"

    if score < 40:
        gauge_color = "#b9aeb2"
    elif score < 55:
        gauge_color = "#d7a2b5"
    elif score < 70:
        gauge_color = "#e58cae"
    elif score < 85:
        gauge_color = "#df6c98"

    st.markdown(
        f"""
        <div class="gauge-wrapper">
            <div
                class="gauge"
                style="
                    background:
                    conic-gradient(
                        {gauge_color} 0deg,
                        {gauge_color} {score * 3.6}deg,
                        #f6e7ed {score * 3.6}deg,
                        #f6e7ed 360deg
                    );
                "
            >
                <div class="gauge-content">
                    <div class="gauge-score">{score}</div>
                    <div class="gauge-unit">SIGNAL SCORE</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 시그널 칩 출력
# ============================================================
def render_signal_chip(text, chip_type="positive"):
    class_name = {
        "positive": "positive-chip",
        "caution": "caution-chip",
        "neutral": "neutral-chip",
    }[chip_type]

    icon = {
        "positive": "💗",
        "caution": "🔍",
        "neutral": "✨",
    }[chip_type]

    st.markdown(
        f"""
        <div class="signal-chip {class_name}">
            <span>{icon}</span>
            <span>{text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 진입 화면
# ============================================================
if not st.session_state.nickname:
    st.markdown(
        """
        <div class="hero">
            <div class="hero-badge">LOVE SIGNAL LAB</div>
            <div class="hero-title">
                메시지 속 <span>썸 시그널</span>을 발견해요
            </div>
            <div class="hero-description">
                상대방의 메시지에 담긴 관심 표현, 대화 지속성,
                정서적인 온도를 분석하고 자연스러운 답장까지 추천해 드려요.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left, center, right = st.columns([1, 1.25, 1])

    with center:
        st.markdown(
            """
            <div class="love-card">
                <div style="
                    text-align:center;
                    font-size:42px;
                    margin-bottom:8px;
                ">
                    💌
                </div>
                <div style="
                    text-align:center;
                    font-weight:800;
                    font-size:20px;
                    margin-bottom:5px;
                ">
                    나만의 시그널 분석실
                </div>
                <div style="
                    text-align:center;
                    color:#8a737c;
                    margin-bottom:20px;
                    font-size:14px;
                ">
                    시작하기 전에 사용할 닉네임을 알려주세요.
                </div>
            """,
            unsafe_allow_html=True,
        )

        nickname = st.text_input(
            "닉네임",
            placeholder="예: 민영",
            label_visibility="collapsed",
        )

        if st.button(
            "분석 시작하기 💗",
            type="primary",
            use_container_width=True,
        ):
            if nickname.strip():
                st.session_state.nickname = nickname.strip()
                st.rerun()
            else:
                st.warning("닉네임을 입력해 주세요.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.markdown(
        f"""
        <div style="padding:8px 0 16px;">
            <div style="
                color:#b34c74;
                font-size:13px;
                font-weight:750;
                letter-spacing:.05em;
            ">
                MY SIGNAL ROOM
            </div>
            <div style="
                font-size:23px;
                font-weight:850;
                margin-top:5px;
            ">
                {st.session_state.nickname}님의 분석실 💗
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    relationship_stage = st.selectbox(
        "현재 관계 단계",
        [
            "소개팅 전",
            "소개팅 직후",
            "연락 중",
            "두 번째 만남 준비",
        ],
    )

    reply_tone = st.selectbox(
        "추천 답장 분위기",
        [
            "부담 없게",
            "다정하게",
            "유머러스하게",
            "적극적으로",
            "예의 바르게",
        ],
    )

    st.divider()

    if st.session_state.score_history:
        average_score = round(
            sum(st.session_state.score_history)
            / len(st.session_state.score_history),
            1,
        )
    else:
        average_score = 0

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "분석 횟수",
            f"{st.session_state.analysis_count}회",
        )

    with col2:
        st.metric(
            "평균 점수",
            f"{average_score}점",
        )

    st.divider()

    if st.button("분석 기록 초기화", use_container_width=True):
        st.session_state.messages = []
        st.session_state.score_history = []
        st.session_state.analysis_count = 0
        st.session_state.celebrated = False
        st.session_state.last_result = None
        st.rerun()

    if st.button("닉네임 변경", use_container_width=True):
        st.session_state.nickname = ""
        st.rerun()


# ============================================================
# 상단 Hero
# ============================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">LOVE SIGNAL LAB</div>
        <div class="hero-title">
            썸 시그널 <span>분석기</span>
        </div>
        <div class="hero-description">
            말 한마디만으로 상대방의 마음을 확정할 수는 없지만,
            대화 속 반복되는 관심과 행동의 흐름은 살펴볼 수 있어요.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 탭
# ============================================================
tab_analysis, tab_stats, tab_about = st.tabs(
    [
        "💌 시그널 분석",
        "📊 분석 리포트",
        "🌷 서비스 소개",
    ]
)


# ============================================================
# 시그널 분석 탭
# ============================================================
with tab_analysis:
    intro_col, status_col = st.columns([2.3, 1])

    with intro_col:
        st.subheader("상대방의 메시지를 분석해 보세요")
        st.caption(
            "받은 메시지를 그대로 입력하면 표현, 길이, 질문 여부와 "
            "대화 흐름을 함께 분석합니다."
        )

    with status_col:
        st.markdown(
            f"""
            <div class="love-card" style="padding:16px 18px;">
                <div style="font-size:12px; color:#a15a75; font-weight:750;">
                    CURRENT SETTING
                </div>
                <div style="margin-top:6px; font-weight:750;">
                    {relationship_stage}
                </div>
                <div style="font-size:13px; color:#846f78; margin-top:3px;">
                    {reply_tone} 답장
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for saved_message in st.session_state.messages:
        with st.chat_message(saved_message["role"]):
            st.markdown(saved_message["content"])

    user_input = st.chat_input(
        "예: 오늘 즐거웠어요! 다음에 또 같이 밥 먹어요 😊"
    )

    if user_input:
        user_input = user_input.strip()

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.status(
                "메시지 속 감정과 대화 흐름을 읽고 있어요 💌",
                expanded=True,
            ) as status:
                st.write("문장 길이와 질문 여부를 확인하고 있어요.")
                time.sleep(0.4)

                st.write("관심 표현과 거리감 표현을 구분하고 있어요.")
                time.sleep(0.4)

                st.write("관계 단계에 맞는 답장을 준비하고 있어요.")
                time.sleep(0.4)

                result = analyze_signal(
                    user_input,
                    relationship_stage,
                )

                reply, reply_tip = recommend_reply(
                    reply_tone,
                    relationship_stage,
                    result,
                )

                status.update(
                    label="분석이 완료되었어요 💗",
                    state="complete",
                    expanded=False,
                )

            result_left, result_right = st.columns([1.2, 1.8])

            with result_left:
                render_signal_gauge(result["score"])

                st.markdown(
                    f"""
                    <div style="text-align:center; margin-top:-10px;">
                        <span style="
                            display:inline-block;
                            padding:7px 14px;
                            border-radius:999px;
                            background:#fff0f5;
                            border:1px solid #f2cfdd;
                            color:#b64a73;
                            font-weight:750;
                            font-size:13px;
                        ">
                            {result["signal_level"]}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with result_right:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <div class="result-label">ANALYSIS RESULT</div>
                        <div class="result-grade">
                            {result["emoji"]} {result["grade"]}
                        </div>
                        <p class="result-summary">
                            {result["summary"]}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.caption(
                    "점수는 메시지 표현을 시각화한 참고값이며 "
                    "상대방의 실제 감정을 확정하지 않습니다."
                )

            st.markdown("### 시그널 구성 요소")

            category_data = pd.DataFrame(
                {
                    "분석 요소": list(result["category_scores"].keys()),
                    "점수": list(result["category_scores"].values()),
                }
            )

            st.bar_chart(
                category_data,
                x="분석 요소",
                y="점수",
                horizontal=True,
                height=280,
            )

            st.caption(
                "대화 지속성은 질문과 다음 약속 표현, 관심 표현은 직접적인 "
                "관심 단어, 정서적 온도는 웃음·이모지·감탄 표현을 반영합니다."
            )

            st.divider()

            signal_col1, signal_col2 = st.columns(2)

            with signal_col1:
                st.markdown("#### 💗 긍정적으로 볼 수 있는 표현")

                if result["positive_signals"]:
                    for signal in result["positive_signals"]:
                        render_signal_chip(signal, "positive")
                else:
                    render_signal_chip(
                        "뚜렷한 긍정 표현은 아직 발견되지 않았어요.",
                        "neutral",
                    )

            with signal_col2:
                st.markdown("#### 🔍 조금 더 살펴볼 부분")

                if result["caution_signals"]:
                    for signal in result["caution_signals"]:
                        render_signal_chip(signal, "caution")
                else:
                    render_signal_chip(
                        "특별히 주의할 표현은 발견되지 않았어요.",
                        "neutral",
                    )

            st.divider()

            st.markdown("### 💌 추천 답장")

            st.markdown(
                f"""
                <div class="reply-card">
                    {reply}
                </div>
                <div class="tip-card">
                    <strong>답장 포인트</strong><br>
                    {reply_tip}
                </div>
                """,
                unsafe_allow_html=True,
            )

            assistant_content = f"""
### {result["emoji"]} {result["grade"]}

**썸 시그널 점수: {result["score"]}점**

{result["summary"]}

#### 추천 답장

> {reply}

💡 **답장 포인트:** {reply_tip}
"""

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_content,
            }
        )

        st.session_state.analysis_count += 1
        st.session_state.score_history.append(result["score"])
        st.session_state.last_result = result

        if (
            st.session_state.analysis_count >= 5
            and not st.session_state.celebrated
        ):
            st.balloons()
            st.toast(
                "벌써 5번이나 분석했어요! 메시지 한 번보다 전체 흐름을 봐주세요 💗"
            )
            st.session_state.celebrated = True


# ============================================================
# 분석 리포트 탭
# ============================================================
with tab_stats:
    st.subheader("나의 썸 시그널 리포트")
    st.caption(
        "분석 결과를 회차별로 비교해 관계의 흐름을 살펴볼 수 있어요."
    )

    if not st.session_state.score_history:
        st.markdown(
            """
            <div class="love-card" style="text-align:center; padding:45px 20px;">
                <div style="font-size:42px; margin-bottom:12px;">🌷</div>
                <div style="font-size:19px; font-weight:800;">
                    아직 분석 기록이 없어요
                </div>
                <div style="color:#88717b; margin-top:8px;">
                    메시지를 분석하면 이곳에 변화 그래프가 나타납니다.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        scores = st.session_state.score_history

        average_score = round(sum(scores) / len(scores), 1)
        highest_score = max(scores)
        latest_score = scores[-1]

        if len(scores) >= 2:
            score_change = scores[-1] - scores[-2]
        else:
            score_change = 0

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "총 분석",
                f"{len(scores)}회",
            )

        with col2:
            st.metric(
                "최근 시그널",
                f"{latest_score}점",
                delta=f"{score_change:+d}점",
            )

        with col3:
            st.metric(
                "평균 시그널",
                f"{average_score}점",
            )

        with col4:
            st.metric(
                "최고 시그널",
                f"{highest_score}점",
            )

        st.markdown("### 회차별 시그널 변화")

        line_data = pd.DataFrame(
            {
                "분석 회차": [
                    f"{index}회"
                    for index in range(1, len(scores) + 1)
                ],
                "시그널 점수": scores,
            }
        )

        st.line_chart(
            line_data,
            x="분석 회차",
            y="시그널 점수",
            height=350,
        )

        st.markdown("### 시그널 단계 분포")

        level_counts = {
            "강한 관심": sum(score >= 85 for score in scores),
            "긍정적": sum(70 <= score < 85 for score in scores),
            "관찰 필요": sum(55 <= score < 70 for score in scores),
            "중립": sum(40 <= score < 55 for score in scores),
            "거리감 가능": sum(score < 40 for score in scores),
        }

        level_data = pd.DataFrame(
            {
                "시그널 단계": list(level_counts.keys()),
                "분석 횟수": list(level_counts.values()),
            }
        )

        st.bar_chart(
            level_data,
            x="시그널 단계",
            y="분석 횟수",
            height=300,
        )

        report_data = pd.DataFrame(
            {
                "회차": list(range(1, len(scores) + 1)),
                "점수": scores,
            }
        )

        report_data["판정"] = report_data["점수"].apply(
            lambda score: (
                "강한 관심"
                if score >= 85
                else "긍정적"
                if score >= 70
                else "관찰 필요"
                if score >= 55
                else "중립"
                if score >= 40
                else "거리감 가능"
            )
        )

        st.markdown("### 분석 기록")

        st.dataframe(
            report_data,
            use_container_width=True,
            hide_index=True,
        )

        st.info(
            "한 번의 높은 점수보다 관심 표현이 여러 대화에서 "
            "일관되게 반복되는지가 더 중요합니다."
        )


# ============================================================
# 서비스 소개 탭
# ============================================================
with tab_about:
    st.markdown(
        """
        <div class="love-card">
            <div style="
                color:#b54b74;
                font-size:13px;
                font-weight:800;
                letter-spacing:.06em;
            ">
                ABOUT THIS PROJECT
            </div>
            <div style="
                font-size:27px;
                font-weight:850;
                margin-top:7px;
                letter-spacing:-.04em;
            ">
                대화 속 작은 관심을 시각적으로 보여주는 서비스
            </div>
            <div style="
                color:#76636b;
                margin-top:12px;
                line-height:1.8;
            ">
                썸 시그널 분석기는 소개팅 전후의 메시지를 분석하여
                대화 지속성, 관심 표현, 정서적인 온도와 구체성을
                직관적으로 보여주는 Streamlit 교육용 프로젝트입니다.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 핵심 기능")

        render_signal_chip(
            "메시지 속 관심 표현과 거리감 표현 분석",
            "positive",
        )
        render_signal_chip(
            "원형 게이지로 썸 시그널 점수 시각화",
            "positive",
        )
        render_signal_chip(
            "분석 요소별 막대그래프 제공",
            "positive",
        )
        render_signal_chip(
            "말투와 관계 단계에 맞는 답장 추천",
            "positive",
        )

    with col2:
        st.markdown("### 사용 기술")

        render_signal_chip(
            "Streamlit session_state와 챗봇 UI",
            "neutral",
        )
        render_signal_chip(
            "조건문과 키워드 기반 텍스트 분석",
            "neutral",
        )
        render_signal_chip(
            "Pandas 데이터프레임과 차트",
            "neutral",
        )
        render_signal_chip(
            "CSS를 활용한 반응형 UI 디자인",
            "neutral",
        )

    st.warning(
        "본 서비스는 교육용 키워드 분석 프로젝트입니다. "
        "상대방의 감정이나 관계의 성공 가능성을 확정하거나 보장하지 않습니다."
    )