# ============================================================
# 💗 썸 시그널 분석기
# 실행 명령어:
# streamlit run .py
# ============================================================

import time
import random
import pandas as pd
import streamlit as st


# ============================================================
# 페이지 기본 설정
# ============================================================
st.set_page_config(
    page_title="썸 시그널 분석기",
    page_icon="💗",
    layout="wide"
)


# ============================================================
# CSS 디자인
# ============================================================
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #777777;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .signal-card {
        padding: 22px;
        border-radius: 18px;
        background-color: #fff5f8;
        border: 1px solid #ffd4df;
        margin-bottom: 15px;
    }

    .result-title {
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .warning-box {
        padding: 16px;
        border-radius: 12px;
        background-color: #fff8e8;
        border: 1px solid #ffe0a3;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 함수 1: 세션 상태 초기화
# ============================================================
def initialize_session_state():
    """앱에서 사용할 세션 상태를 초기화합니다."""

    default_values = {
        "nickname": "",
        "messages": [],
        "history": [],
        "score_history": [],
        "analysis_count": 0,
        "celebrated": False,
        "last_result": None
    }

    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================
# 함수 2: 메시지 전처리
# ============================================================
def clean_message(message):
    """입력한 메시지의 앞뒤 공백을 제거합니다."""

    return message.strip()


# ============================================================
# 함수 3: 썸 시그널 분석
# ============================================================
def analyze_signal(message, relationship_stage):
    """
    상대방 메시지의 표현을 기반으로 썸 시그널 점수를 계산합니다.

    주의:
    이 결과는 키워드 기반 참고용 분석이며,
    상대방의 실제 감정을 확정하지 않습니다.
    """

    message = clean_message(message)
    lower_message = message.lower()

    score = 50
    positive_signals = []
    caution_signals = []

    # --------------------------------------------------------
    # 긍정 신호 키워드
    # --------------------------------------------------------
    positive_keywords = {
        "보고 싶": 12,
        "또 보": 12,
        "다음에": 10,
        "같이": 7,
        "즐거웠": 10,
        "재밌었": 9,
        "좋았": 8,
        "궁금": 6,
        "뭐 해": 6,
        "잘 들어갔": 7,
        "조심히": 5,
        "연락해": 6,
        "기다릴": 8,
        "시간 돼": 10,
        "언제 시간": 11,
        "맛있는 거": 6,
        "생각나": 10,
        "ㅋㅋ": 3,
        "ㅎㅎ": 3,
        "😊": 4,
        "😍": 7,
        "❤️": 8,
        "💕": 8,
        "🥰": 8
    }

    for keyword, value in positive_keywords.items():
        if keyword in lower_message:
            score += value
            positive_signals.append(f"'{keyword}' 표현이 포함되어 있습니다.")

    # --------------------------------------------------------
    # 주의 신호 키워드
    # --------------------------------------------------------
    negative_keywords = {
        "바빠": -7,
        "나중에": -4,
        "언젠가": -5,
        "글쎄": -7,
        "모르겠": -5,
        "피곤": -4,
        "연락할게": -3,
        "시간 되면": -5,
        "기회 되면": -6,
        "네": -2,
        "넵": -2,
        "ㅇㅇ": -5,
        "아니": -3
    }

    for keyword, value in negative_keywords.items():
        if keyword in lower_message:
            score += value
            caution_signals.append(f"'{keyword}' 표현은 상황에 따라 거리감이 느껴질 수 있습니다.")

    # --------------------------------------------------------
    # 문장 구조 분석
    # --------------------------------------------------------
    question_count = message.count("?") + message.count("？")

    if question_count > 0:
        score += 8
        positive_signals.append("질문이 있어 대화를 이어가려는 모습이 보입니다.")
    else:
        caution_signals.append("질문이 없어 대화가 자연스럽게 종료될 가능성이 있습니다.")

    # 메시지 길이 분석
    message_length = len(message)

    if message_length >= 40:
        score += 7
        positive_signals.append("비교적 구체적이고 긴 메시지입니다.")
    elif message_length >= 20:
        score += 3
        positive_signals.append("성의 있는 길이의 메시지입니다.")
    elif message_length <= 5:
        score -= 12
        caution_signals.append("답장이 매우 짧아 추가적인 맥락 확인이 필요합니다.")
    elif message_length <= 10:
        score -= 5
        caution_signals.append("메시지가 다소 짧은 편입니다.")

    # 이모티콘 분석
    emoji_list = ["😊", "😄", "😍", "🥰", "❤️", "💕", "☺️", "😆", "ㅋㅋ", "ㅎㅎ"]

    if any(emoji in message for emoji in emoji_list):
        score += 5
        positive_signals.append("웃음 표현이나 이모티콘으로 부드러운 분위기를 만들고 있습니다.")

    # 관계 단계에 따른 점수 보정
    if relationship_stage == "소개팅 전":
        score -= 2
    elif relationship_stage == "소개팅 직후":
        score += 3
    elif relationship_stage == "연락 중":
        score += 2
    elif relationship_stage == "두 번째 만남 준비":
        score += 5

    # 점수 범위 제한
    score = max(0, min(score, 100))

    # 중복 제거
    positive_signals = list(dict.fromkeys(positive_signals))
    caution_signals = list(dict.fromkeys(caution_signals))

    # 분석 문구 결정
    if score >= 85:
        grade = "매우 높은 관심 신호"
        summary = "상대방이 대화를 적극적으로 이어가고 싶어 하는 표현이 여러 개 발견되었습니다."
        emoji = "💖"

    elif score >= 70:
        grade = "긍정적인 관심 신호"
        summary = "호감으로 볼 수 있는 표현이 있으나, 대화 흐름을 함께 살펴보는 것이 좋습니다."
        emoji = "💗"

    elif score >= 55:
        grade = "조금 더 지켜볼 단계"
        summary = "긍정적인 요소는 있지만 아직 상대방의 마음을 단정하기에는 정보가 부족합니다."
        emoji = "💓"

    elif score >= 40:
        grade = "중립적인 신호"
        summary = "예의 있는 답장일 가능성이 있습니다. 한두 번의 메시지만으로 판단하지 않는 것이 좋습니다."
        emoji = "💬"

    else:
        grade = "거리감이 느껴질 수 있는 신호"
        summary = "현재 메시지만 보면 적극적인 관심은 크지 않을 수 있습니다. 무리하게 대화를 이어가지는 마세요."
        emoji = "🩶"

    return {
        "score": score,
        "grade": grade,
        "summary": summary,
        "emoji": emoji,
        "positive_signals": positive_signals,
        "caution_signals": caution_signals
    }


# ============================================================
# 함수 4: 답장 추천
# ============================================================
def recommend_reply(message, tone, relationship_stage, result):
    """분석 결과와 선택한 말투에 맞는 답장을 추천합니다."""

    score = result["score"]

    reply_options = {
        "부담 없게": [
            "저도 즐거웠어요! 조심히 들어가셨죠? 다음에 또 편하게 봬요 😊",
            "오늘 즐거웠어요. 들어가시는 길 조심하시고 다음에 또 이야기 나눠요!",
            "저도 좋은 시간이었어요! 남은 하루도 편하게 보내세요 😊"
        ],

        "다정하게": [
            "저도 오늘 정말 즐거웠어요 😊 덕분에 시간 가는 줄 몰랐네요. 조심히 들어가세요!",
            "오늘 만나서 정말 반가웠어요. 이야기 나누는 시간이 편하고 좋았어요 💗",
            "저도 즐거웠어요! 집에 잘 들어가셨는지 궁금했어요. 푹 쉬세요 😊"
        ],

        "유머러스하게": [
            "저도 즐거웠어요! 시간 순삭의 범인은 아무래도 우리였던 것 같네요 😆",
            "오늘 정말 재미있었어요. 다음에는 더 맛있는 메뉴로 2차 면접 진행하시죠 😄",
            "저도 즐거웠어요! 대화가 너무 잘 통해서 시간 확인을 깜빡했네요 ㅋㅋ"
        ],

        "적극적으로": [
            "저도 정말 즐거웠어요! 다음에 또 만나고 싶은데 이번 주말은 어떠세요? 😊",
            "오늘 이야기 나누는 시간이 좋았어요. 괜찮으시면 다음에는 제가 맛있는 곳 찾아볼게요!",
            "저도 즐거웠어요. 다음에 또 뵙고 싶은데 시간 괜찮은 날 알려주세요 💗"
        ],

        "예의 바르게": [
            "저도 오늘 즐거운 시간이었습니다. 조심히 들어가시고 편안한 저녁 보내세요.",
            "오늘 만나 뵙게 되어 반가웠습니다. 좋은 시간 만들어 주셔서 감사합니다 😊",
            "저도 즐거웠습니다. 귀가길 조심하시고 다음에 또 좋은 기회로 뵙겠습니다."
        ]
    }

    selected_replies = reply_options.get(tone, reply_options["부담 없게"])
    reply = random.choice(selected_replies)

    # 호감 점수가 낮을 때는 적극적인 말투를 조금 완화
    if score < 45 and tone == "적극적으로":
        reply = (
            "오늘 만나서 반가웠어요! 조심히 들어가시고 "
            "편안한 저녁 보내세요 😊"
        )

    # 관계 단계별 보조 문장
    if relationship_stage == "소개팅 전":
        tip = "소개팅 전에는 너무 긴 답장보다 약속 시간과 장소를 명확하게 확인하는 것이 좋습니다."

    elif relationship_stage == "소개팅 직후":
        tip = "소개팅 직후에는 즐거웠다는 감정과 귀가 여부를 함께 묻는 답장이 자연스럽습니다."

    elif relationship_stage == "연락 중":
        tip = "상대방의 답장 길이와 속도에 맞춰 비슷한 정도의 텐션을 유지해 보세요."

    else:
        tip = "두 번째 만남을 준비 중이라면 구체적인 날짜나 활동을 제안하는 것이 좋습니다."

    return reply, tip


# ============================================================
# 함수 5: 초기화
# ============================================================
initialize_session_state()


# ============================================================
# 진입 게이트
# ============================================================
if not st.session_state.nickname:
    st.markdown(
        '<div class="main-title">💗 썸 시그널 분석기</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">'
        '상대방의 메시지 속 호감 신호를 분석하고 자연스러운 답장을 추천해 드려요.'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            "https://images.unsplash.com/photo-1518199266791-5375a83190b7"
            "?auto=format&fit=crop&w=1200&q=80",
            use_container_width=True
        )

        name = st.text_input(
            "사용할 닉네임을 입력하세요",
            placeholder="예: 민영"
        )

        if st.button(
            "💓 두근두근 시작하기",
            type="primary",
            use_container_width=True
        ) and name.strip():

            st.session_state.nickname = name.strip()
            st.rerun()

        st.caption(
            "입력한 메시지는 현재 Streamlit 세션에서만 분석됩니다."
        )

    st.stop()


# ============================================================
# 사이드바
# ============================================================
with st.sidebar:
    st.title(f"💗 {st.session_state.nickname}님의 분석실")

    relationship_stage = st.selectbox(
        "현재 관계 단계",
        [
            "소개팅 전",
            "소개팅 직후",
            "연락 중",
            "두 번째 만남 준비"
        ]
    )

    reply_tone = st.selectbox(
        "원하는 답장 분위기",
        [
            "부담 없게",
            "다정하게",
            "유머러스하게",
            "적극적으로",
            "예의 바르게"
        ]
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "분석 횟수",
            st.session_state.analysis_count
        )

    with col2:
        if st.session_state.score_history:
            average_score = round(
                sum(st.session_state.score_history)
                / len(st.session_state.score_history)
            )
        else:
            average_score = 0

        st.metric(
            "평균 점수",
            f"{average_score}점"
        )

    st.divider()

    if st.button(
        "🗑️ 분석 기록 초기화",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.session_state.history = []
        st.session_state.score_history = []
        st.session_state.analysis_count = 0
        st.session_state.celebrated = False
        st.session_state.last_result = None
        st.rerun()

    if st.button(
        "🚪 닉네임 변경",
        use_container_width=True
    ):
        st.session_state.nickname = ""
        st.rerun()


# ============================================================
# 메인 제목
# ============================================================
st.markdown(
    '<div class="main-title">💗 썸 시그널 분석기</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    '메시지 하나만으로 마음을 확정할 수는 없지만, 대화 속 표현을 함께 살펴볼 수 있어요.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 탭 구성
# ============================================================
tab_analysis, tab_stats, tab_about = st.tabs(
    [
        "💌 시그널 분석",
        "📊 분석 통계",
        "ℹ️ 서비스 소개"
    ]
)


# ============================================================
# 탭 1: 시그널 분석
# ============================================================
with tab_analysis:

    st.subheader("상대방에게 받은 메시지를 입력해 주세요")

    st.caption(
        f"현재 단계: {relationship_stage} · "
        f"답장 스타일: {reply_tone}"
    )

    # 기존 대화 기록 출력
    for message_data in st.session_state.messages:

        with st.chat_message(message_data["role"]):
            st.markdown(message_data["content"])

            if message_data.get("score") is not None:
                st.progress(message_data["score"] / 100)
                st.caption(
                    f"참고용 썸 시그널 점수: "
                    f"{message_data['score']}점"
                )

    user_input = st.chat_input(
        "예: 오늘 즐거웠어요! 다음에 또 같이 밥 먹어요 😊"
    )

    if user_input:

        cleaned_input = clean_message(user_input)

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {
                "role": "user",
                "content": cleaned_input
            }
        )

        with st.chat_message("user"):
            st.markdown(cleaned_input)

        # AI 분석 과정
        with st.chat_message("assistant"):

            with st.status(
                "💌 메시지 속 썸 시그널을 분석하고 있어요...",
                expanded=True
            ) as status:

                st.write("1️⃣ 메시지의 길이와 질문 여부를 확인하고 있어요.")
                time.sleep(0.5)

                st.write("2️⃣ 호감 표현과 거리감 표현을 찾고 있어요.")
                time.sleep(0.5)

                st.write("3️⃣ 현재 관계 단계에 맞춰 결과를 정리하고 있어요.")
                time.sleep(0.5)

                analysis_result = analyze_signal(
                    cleaned_input,
                    relationship_stage
                )

                recommended_reply, reply_tip = recommend_reply(
                    cleaned_input,
                    reply_tone,
                    relationship_stage,
                    analysis_result
                )

                status.update(
                    label="✅ 분석이 완료되었습니다!",
                    state="complete",
                    expanded=False
                )

            # 분석 결과 화면
            st.markdown(
                f"""
                <div class="signal-card">
                    <div class="result-title">
                        {analysis_result["emoji"]}
                        {analysis_result["grade"]}
                    </div>
                    <p>{analysis_result["summary"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.metric(
                "참고용 썸 시그널 점수",
                f"{analysis_result['score']}점"
            )

            st.progress(analysis_result["score"] / 100)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 💗 긍정적으로 볼 수 있는 표현")

                if analysis_result["positive_signals"]:
                    for signal in analysis_result["positive_signals"]:
                        st.success(signal)
                else:
                    st.info(
                        "뚜렷한 긍정 표현은 발견되지 않았습니다."
                    )

            with col2:
                st.markdown("#### 🔍 조금 더 살펴볼 부분")

                if analysis_result["caution_signals"]:
                    for signal in analysis_result["caution_signals"]:
                        st.warning(signal)
                else:
                    st.info(
                        "특별히 주의할 표현은 발견되지 않았습니다."
                    )

            st.markdown("#### ✉️ 추천 답장")

            st.code(
                recommended_reply,
                language=None
            )

            st.caption(f"💡 답장 팁: {reply_tip}")

            st.info(
                "이 결과는 메시지 표현을 기반으로 한 참고용 분석입니다. "
                "상대방의 실제 감정이나 의도를 확정하지 않습니다."
            )

            # AI 메시지 저장용 콘텐츠
            assistant_content = f"""
### {analysis_result["emoji"]} {analysis_result["grade"]}

**썸 시그널 점수:** {analysis_result["score"]}점

{analysis_result["summary"]}

#### ✉️ 추천 답장

> {recommended_reply}

💡 **답장 팁:** {reply_tip}
"""

        # AI 응답 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_content,
                "score": analysis_result["score"]
            }
        )

        # 통계 저장
        st.session_state.analysis_count += 1

        st.session_state.history.append(
            st.session_state.analysis_count
        )

        st.session_state.score_history.append(
            analysis_result["score"]
        )

        st.session_state.last_result = analysis_result

        # 분석 5회 달성 시 풍선 효과
        if (
            st.session_state.analysis_count >= 5
            and not st.session_state.celebrated
        ):
            st.balloons()
            st.success(
                "🎉 썸 시그널을 5번 분석했어요! "
                "이제 메시지의 흐름도 함께 살펴보세요."
            )
            st.session_state.celebrated = True


# ============================================================
# 탭 2: 분석 통계
# ============================================================
with tab_stats:

    st.subheader("📊 나의 썸 시그널 분석 기록")

    if not st.session_state.score_history:
        st.info(
            "아직 분석 기록이 없습니다. "
            "상대방의 메시지를 분석하면 통계가 표시됩니다."
        )

    else:
        total_count = st.session_state.analysis_count
        latest_score = st.session_state.score_history[-1]
        average_score = round(
            sum(st.session_state.score_history)
            / len(st.session_state.score_history),
            1
        )
        highest_score = max(st.session_state.score_history)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "총 분석 횟수",
                f"{total_count}회"
            )

        with col2:
            st.metric(
                "최근 점수",
                f"{latest_score}점"
            )

        with col3:
            st.metric(
                "평균 점수",
                f"{average_score}점"
            )

        with col4:
            st.metric(
                "최고 점수",
                f"{highest_score}점"
            )

        st.divider()

        # 데이터프레임 생성
        chart_data = pd.DataFrame(
            {
                "분석 회차": list(
                    range(
                        1,
                        len(st.session_state.score_history) + 1
                    )
                ),
                "썸 시그널 점수": st.session_state.score_history
            }
        )

        st.markdown("### 💓 분석 회차별 시그널 점수")

        st.line_chart(
            chart_data,
            x="분석 회차",
            y="썸 시그널 점수"
        )

        st.markdown("### 📋 분석 기록")

        display_data = chart_data.copy()
        display_data["판정"] = display_data[
            "썸 시그널 점수"
        ].apply(
            lambda score:
            "매우 긍정적"
            if score >= 85
            else "긍정적"
            if score >= 70
            else "관찰 필요"
            if score >= 55
            else "중립"
            if score >= 40
            else "거리감 가능"
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "점수의 한 번 한 번보다 여러 메시지에서 나타나는 "
            "전체적인 변화와 대화 흐름을 살펴보는 것이 더 중요합니다."
        )


# ============================================================
# 탭 3: 서비스 소개
# ============================================================
with tab_about:

    st.subheader("💗 썸 시그널 분석기란?")

    st.markdown(
        """
        **썸 시그널 분석기**는 소개팅 전후에 받은 메시지를 분석하여
        대화 속 긍정적인 표현과 주의해서 살펴볼 표현을 알려주는
        Streamlit 기반 커뮤니케이션 서비스입니다.

        상대방의 메시지를 입력하면 다음 내용을 확인할 수 있습니다.

        - 메시지 속 호감 표현 탐색
        - 질문 여부와 메시지 길이 분석
        - 참고용 썸 시그널 점수 제공
        - 관계 단계와 말투에 맞는 답장 추천
        - 분석 점수 변화 통계 제공
        """
    )

    st.divider()

    st.markdown("### 🛠️ 프로젝트에 사용된 기술")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            #### Streamlit 기능

            - `st.session_state`
            - `st.chat_message`
            - `st.chat_input`
            - `st.status`
            - `st.tabs`
            - `st.sidebar`
            - `st.metric`
            - `st.line_chart`
            - `st.progress`
            - `st.balloons`
            """
        )

    with col2:
        st.markdown(
            """
            #### Python 기능

            - 함수 정의
            - 조건문
            - 반복문
            - 딕셔너리
            - 리스트
            - 문자열 분석
            - 예외 상황 처리
            - Pandas 데이터프레임
            """
        )

    st.divider()

    st.markdown("### ⚠️ 이용 안내")

    st.warning(
        "본 서비스는 메시지의 단어와 문장 구조를 기준으로 분석하는 "
        "교육용 프로젝트입니다. 상대방의 실제 마음이나 관계의 성공 여부를 "
        "판단하거나 보장하지 않습니다."
    )

    st.markdown(
        """
        좋은 관계에서는 특정 메시지 하나보다 다음 요소가 더 중요합니다.

        - 서로의 의사를 존중하는 태도
        - 일관된 관심과 행동
        - 부담스럽지 않은 소통
        - 명확하고 솔직한 표현
        """
    )