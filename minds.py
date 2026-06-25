import streamlit as st
import pandas as pd
import altair as alt
import json
import plotly.express as px

st.set_page_config(layout="wide", page_title="보이지 않는 마음을 찾아서", page_icon="🧭")

# =========================
# 변경: 디자인 시스템 - 색상/타이포 토큰 + 전역 CSS
# =========================
INK = "#1A2233"      # 헤드라인/사이드바 배경
BG = "#F4F6FB"        # 페이지 배경 (차가운 라벤더그레이)
SURFACE = "#FFFFFF"   # 카드 배경
PRIMARY = "#3654A6"   # 메인 포인트 (기관)
TEAL = "#2F8F87"      # 양호/보조 포인트
CORAL = "#D64545"     # 위험(데이터 인코딩 전용)
SLATE = "#5B6B8C"     # 보조 포인트
MUTED = "#6B7280"     # 보조 텍스트
BORDER = "#E3E7F0"    # 테두리

st.markdown(f"""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@500;700;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Pretendard', -apple-system, sans-serif;
}}
[data-testid="stAppViewContainer"] {{ background-color: {BG}; }}
.block-container {{ padding-top: 1.2rem; max-width: 1280px; }}

h1, h2, h3 {{ font-family: 'Noto Serif KR', serif; color: {INK}; }}

/* 사이드바: 잉크색 패널 */
[data-testid="stSidebar"] {{ background-color: {INK}; }}
[data-testid="stSidebar"] * {{ color: #E7EBF5 !important; }}
[data-testid="stSidebar"] label {{ font-weight: 600; }}
[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.15); }}

/* 안내 카드(st.info) */
[data-testid="stAlert"] {{
    background-color: #EEF2FB;
    border-left: 4px solid {PRIMARY};
    border-radius: 10px;
}}

/* 탭 */
.stTabs [data-baseweb="tab-list"] {{ gap: 6px; border-bottom: 1px solid {BORDER}; }}
.stTabs [data-baseweb="tab"] {{
    height: 46px; background-color: transparent;
    border-radius: 8px 8px 0 0; color: {MUTED}; font-weight: 700;
}}
.stTabs [aria-selected="true"] {{
    color: {PRIMARY} !important;
    border-bottom: 3px solid {PRIMARY} !important;
}}

/* 표 */
[data-testid="stDataFrame"] {{ border-radius: 10px; border: 1px solid {BORDER}; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)


# 변경: Altair 차트 공통 스타일(폰트/색/그리드)을 한 군데서 적용하는 헬퍼
def style_chart(chart):
    FONT = "Pretendard, -apple-system, sans-serif"  # 변경: 폴백 폰트 추가 (Pretendard 미로딩 시 글자가 사라지는 문제 방지)
    return (
        chart
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelFont=FONT, titleFont=FONT,
            labelColor=MUTED, titleColor=INK,
            gridColor=BORDER, domainColor=BORDER, tickColor=BORDER,
        )
        .configure_title(font=FONT, fontSize=15, fontWeight=700, color=INK, anchor="start")
        .configure_legend(labelFont=FONT, titleFont=FONT)
    )


# 변경: 카드형 지표(eyebrow + 큰 숫자 + 좌측 컬러 바)를 그리는 헬퍼
def metric_card(col, eyebrow, value, accent=PRIMARY):
    col.markdown(
        f"""
        <div style="background:{SURFACE}; border:1px solid {BORDER}; border-radius:12px;
                    padding:18px 22px; position:relative; overflow:hidden;">
            <div style="position:absolute; left:0; top:0; bottom:0; width:5px; background:{accent};"></div>
            <div style="font-size:12px; font-weight:700; letter-spacing:0.04em; color:{MUTED};
                        text-transform:uppercase; margin-bottom:8px;">{eyebrow}</div>
            <div style="font-size:28px; font-weight:800; color:{INK};">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# 변경: 탭 내부 섹션 제목(작은 라벨 + 타이틀)을 그리는 헬퍼 - st.subheader 대체
def section_header(eyebrow, title):
    st.markdown(
        f"""
        <div style="margin: 6px 0 14px 0;">
            <div style="font-size:12px; font-weight:700; letter-spacing:0.08em; color:{TEAL};
                        text-transform:uppercase;">{eyebrow}</div>
            <div style="font-size:19px; font-weight:700; color:{INK};">{title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )




# 변경: 히어로 배너 - 잉크색 배경 + 세리프 타이틀 + 틸→블루 그라데이션 언더라인
st.markdown(
    f"""
    <div style="background:linear-gradient(135deg, {INK} 0%, #233357 100%);
                border-radius:18px; padding:44px 40px 34px 40px; margin-bottom:22px;">
        <div style="color:#8FC4BD; font-size:13px; font-weight:700; letter-spacing:0.18em;
                    text-transform:uppercase; margin-bottom:10px;">MENTAL HEALTH ACCESS DASHBOARD</div>
        <div style="font-family:'Noto Serif KR', serif; font-size:36px; font-weight:700;
                    color:#FFFFFF; line-height:1.35;">보이지 않는 마음을 찾아서</div>
        <div style="height:4px; width:64px; margin:16px 0; border-radius:2px;
                    background:linear-gradient(90deg, {TEAL}, {PRIMARY});"></div>
        <div style="color:#C7CEDD; font-size:15px; max-width:640px; line-height:1.7;">
            인구 대비 정신건강 관련기관이 부족한 지역을 데이터로 짚어봅니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# 변경: 데이터 출처/범위 안내 - 좌측 컬러 바가 있는 카드 형태로 통일 (기존 st.info 2개 대체)
st.markdown(
    f"""
    <div style="background:{SURFACE}; border:1px solid {BORDER}; border-left:4px solid {PRIMARY};
                border-radius:10px; padding:18px 22px; margin-bottom:26px;">
        <div style="font-weight:700; color:{INK}; font-size:14px; margin-bottom:8px;">ℹ️ 데이터 안내</div>
        <div style="color:{MUTED}; font-size:13.5px; line-height:1.8;">
            이 대시보드의 <b>기관수</b>는 보건복지부 산하 <b>국립정신건강센터</b>가 운영하는
            국가정신건강정보포털(mentalhealth.go.kr)의 "정신건강 관련기관" 목록을 기준으로 합니다.<br><br>
            의원·병원·종합병원·상급종합병원 같은 <b>의료기관</b>뿐 아니라, 보건소·정신건강복지센터·자살예방센터·
            중독관리통합지원센터 등 <b>진단 여부와 무관하게 이용 가능한 공공 상담·예방기관</b>도 포함되어 있어
            실제 '정신병원' 수(의료기관 수)와는 차이가 있을 수 있습니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# 시도 매핑 테이블 (긴 이름 -> 짧은 이름)
# =========================
SIDO_MAP = {
    "서울특별시": "서울", "부산광역시": "부산", "대구광역시": "대구", "인천광역시": "인천",
    "광주광역시": "광주", "대전광역시": "대전", "울산광역시": "울산", "세종특별자치시": "세종",
    "경기도": "경기", "강원도": "강원", "강원특별자치도": "강원",
    "충청북도": "충북", "충청남도": "충남",
    "전라북도": "전북", "전북특별자치도": "전북", "전라남도": "전남",
    "경상북도": "경북", "경상남도": "경남",
    "제주특별자치도": "제주", "제주도": "제주",
}

# 짧은 이름 -> GeoJSON(NAME_1) 영문 이름
# 주의: 이 GeoJSON에는 세종특별자치시 폴리곤이 없어 세종은 지도에 표시되지 않음
ENG_SIDO_MAP = {
    "서울": "Seoul", "부산": "Busan", "대구": "Daegu", "인천": "Incheon",
    "광주": "Gwangju", "대전": "Daejeon", "울산": "Ulsan",
    "경기": "Gyeonggi-do", "강원": "Gangwon-do",
    "충북": "Chungcheongbuk-do", "충남": "Chungcheongnam-do",
    "전북": "Jeollabuk-do", "전남": "Jeollanam-do",
    "경북": "Gyeongsangbuk-do", "경남": "Gyeongsangnam-do",
    "제주": "Jeju",
}

# 변경: 기관구분(13종)을 3개 큰 유형으로 묶는 매핑
# - 의료기관: 실제 진료/입원이 이뤄지는 곳 (진단 여부와 상관없이 "환자"가 되어 방문)
# - 공공상담예방기관: 진단 여부와 무관하게 일반 주민도 상담/예방 서비스 이용 가능
# - 요양재활시설: 이미 진단받은 정신질환자 대상의 요양/재활시설
INSTITUTION_TYPE_MAP = {
    "의원": "의료기관", "병원": "의료기관", "종합병원": "의료기관", "상급종합병원": "의료기관",
    "국립": "의료기관", "공립": "의료기관",
    "보건소": "공공상담예방기관", "기초정신건강복지센터": "공공상담예방기관",
    "광역정신건강복지센터": "공공상담예방기관", "자살예방센터": "공공상담예방기관",
    "중독관리통합지원센터": "공공상담예방기관",
    "정신요양시설": "요양재활시설", "정신재활시설": "요양재활시설",
}


pop_df = pd.read_excel("data/202412_202412_주민등록인구및세대현황_연간.xlsx")
pop_df.columns = pop_df.columns.str.strip()
pop_df["행정기관"] = pop_df["행정기관"].str.strip()
pop_df = pop_df[pop_df["행정기관"] != "전국"]
pop_df["시도"] = pop_df["행정기관"].map(SIDO_MAP)
pop_df["총인구수"] = pop_df["총인구수"].astype(str).str.replace(",", "").astype(int)
POPULATION_2024 = dict(zip(pop_df["시도"], pop_df["총인구수"]))

# =========================
# 1. 기관 데이터
# =========================
center_df = pd.read_csv(
    "data/보건복지부 국립정신건강센터_정신건강 관련기관 정보_20220301.csv",
    encoding="cp949"
)
center_df["시도"] = center_df["시도"].map(SIDO_MAP)
center_df = center_df.dropna(subset=["시도"])
center_df["기관유형"] = center_df["기관구분"].map(INSTITUTION_TYPE_MAP)  # 변경: 기관유형 컬럼 추가

# 변경: 사이드바 필터 시작 (기관 유형 먼저 배치)
# 변경: 사이드바 헤더 - 작은 라벨 스타일로 변경
st.sidebar.markdown(
    """<div style="font-size:12px; font-weight:700; letter-spacing:0.1em;
    text-transform:uppercase; color:#8FC4BD; margin-bottom:4px;">FILTER</div>
    <div style="font-size:17px; font-weight:700; color:#fff; margin-bottom:14px;">🔍 데이터 필터</div>""",
    unsafe_allow_html=True
)

institution_type_options = ["전체", "의료기관", "공공상담예방기관", "요양재활시설"]
selected_institution_type = st.sidebar.selectbox("기관 유형", institution_type_options)

filtered_center_df = center_df
if selected_institution_type != "전체":
    filtered_center_df = center_df[center_df["기관유형"] == selected_institution_type]

region_count = filtered_center_df["시도"].value_counts().reset_index()  # 변경: center_df -> filtered_center_df
region_count.columns = ["시도", "기관수"]

chart_center = style_chart(
    alt.Chart(region_count)
    .mark_bar(cornerRadiusEnd=3)  # 변경: 막대 끝 모서리를 살짝 둥글게
    .encode(
        x="기관수:Q",
        y=alt.Y("시도:N", sort="-x", title=None),
        color=alt.Color("시도:N", legend=None, scale=alt.Scale(scheme="category20")),
        tooltip=["시도", "기관수"]
    )
    .properties(title=f"지역별 정신건강 기관 수 ({selected_institution_type})")
)

# =========================
# 2. 환자 데이터
# =========================
patient_df = pd.read_csv(
    "data/건강보험심사평가원_시군구별 성별 연령별 주요 정실질환 통계 2024.csv",
    encoding="cp949"
)
patient_df["시도"] = patient_df["시도"].map(SIDO_MAP).fillna(patient_df["시도"])

# 변경: 질환 / 연령대 / 성별 필터 (기관 유형 필터 다음에 이어서 배치, 헤더는 위에서 한 번만 호출)
disease_options = ["전체"] + sorted(patient_df["상별구분"].unique().tolist())
selected_disease = st.sidebar.selectbox("질환 선택", disease_options)

# 연령구분이 문자열 카테고리라 select_slider로 두 지점(시작~끝)을 선택하게 함
AGE_ORDER = [
    "0~9세", "10~19세", "20~29세", "30~39세", "40~49세", "50~59세",
    "60~69세", "70~79세", "80~89세", "90~99세", "100세이상"
]
age_start, age_end = st.sidebar.select_slider(
    "연령대 범위",
    options=AGE_ORDER,
    value=(AGE_ORDER[0], AGE_ORDER[-1])
)
selected_ages = AGE_ORDER[AGE_ORDER.index(age_start): AGE_ORDER.index(age_end) + 1]

# 변경: 성별 필터 추가
gender_options = ["전체"] + sorted(patient_df["성별"].unique().tolist())
selected_gender = st.sidebar.selectbox("성별", gender_options)

# 변경: 선택한 질환 / 연령대 / 성별로 환자 데이터 필터링
filtered_patient_df = patient_df[patient_df["연령구분"].isin(selected_ages)]
if selected_disease != "전체":
    filtered_patient_df = filtered_patient_df[filtered_patient_df["상별구분"] == selected_disease]
if selected_gender != "전체":
    filtered_patient_df = filtered_patient_df[filtered_patient_df["성별"] == selected_gender]

patient_region = (
    filtered_patient_df.groupby("시도")["환자수"]
    .sum()
    .reset_index()
)

chart_patient = style_chart(
    alt.Chart(patient_region)
    .mark_bar(cornerRadiusEnd=3)  # 변경: 막대 끝 모서리를 살짝 둥글게 (기관수 차트와 통일)
    .encode(
        x=alt.X("환자수:Q", title="환자 수"),
        y=alt.Y("시도:N", sort="-x", title=None),
        color=alt.Color("시도:N", legend=None, scale=alt.Scale(scheme="category20")),
        tooltip=[
            alt.Tooltip("시도:N"),
            alt.Tooltip("환자수:Q", format=",")
        ]
    )
    .properties(title=f"지역별 환자 수 ({selected_disease} / {age_start}~{age_end} / {selected_gender})")
)

# =========================
# 3. 사각지대 지표 계산 (인구 10만명당 기관수)
# =========================
merged = region_count.copy()
merged["인구수"] = merged["시도"].map(POPULATION_2024)
merged["인구10만명당기관수"] = merged["기관수"] / (merged["인구수"] / 100_000)
merged = merged.merge(patient_region, on="시도", how="left")
merged["환자수"] = merged["환자수"].fillna(0)  # 변경: 필터링으로 환자수가 0인 시도가 생길 수 있어 NaN 방지

top5 = merged.sort_values("인구10만명당기관수", ascending=True).head(5)

chart_gap = style_chart(
    alt.Chart(merged.sort_values("인구10만명당기관수", ascending=True))
    .mark_bar(cornerRadiusEnd=3)
    .encode(
        x=alt.X("인구10만명당기관수:Q", title="인구 10만명당 기관수"),
        y=alt.Y("시도:N", sort="x", title=None),
        color=alt.Color(
            "인구10만명당기관수:Q",
            scale=alt.Scale(range=[CORAL, "#F8D8D2"]),  # 변경: 디자인 토큰의 CORAL을 사용해 낮음=코랄(위험), 높음=옅은색으로 통일
            title="인구10만명당 기관수"
        ),
        tooltip=["시도", alt.Tooltip("인구10만명당기관수:Q", format=".2f")]
    )
    .properties(title=f"사각지대 위험도 (인구 10만명당 기관수 - {selected_institution_type}, 낮을수록 위험)")
)

with open("data/korea_geo.json", encoding="utf-8") as f:
    korea_geo = json.load(f)
merged["NAME_1"] = merged["시도"].map(ENG_SIDO_MAP)

fig = px.choropleth(
    merged,
    geojson=korea_geo,
    locations="NAME_1",
    featureidkey="properties.NAME_1",
    color="인구10만명당기관수",
    color_continuous_scale=[[0, CORAL], [1, "#F8D8D2"]],  # 변경: 디자인 토큰 CORAL 기준 그라데이션으로 통일 (낮음=코랄, 높음=옅은색)
    hover_name="시도",
    hover_data={"NAME_1": False, "인구10만명당기관수": ":.2f"},
    labels={"인구10만명당기관수": "인구 10만명당 기관수"},
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    title=dict(
        text=f"정신건강 복지 사각지대 지도 ({selected_institution_type})",
        font=dict(family="Pretendard, sans-serif", size=16, color=INK)
    ),
    font=dict(family="Pretendard, sans-serif", color=MUTED),  # 변경: 전체 폰트를 디자인 시스템 폰트로 통일
    paper_bgcolor="rgba(0,0,0,0)",  # 변경: 배경을 투명하게 해서 페이지 배경(BG)과 자연스럽게 어울리도록
    plot_bgcolor="rgba(0,0,0,0)",
    width=600,
    height=600,
    margin=dict(l=0, r=0, t=44, b=0),
)

# =========================
# 4. 화면 배치 (변경: 전체를 tab 3개로 재구성)
# =========================
tab1, tab2, tab3 = st.tabs(["📊 현황", "🚨 사각지대 위험도", "🗺 지도"])

with tab1:
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        section_header("INFRASTRUCTURE", f"🏥 지역별 정신건강 기관 수 · {selected_institution_type}")
        st.altair_chart(chart_center, use_container_width=True)
    with col2:
        section_header("PATIENTS", f"🧑‍⚕️ 지역별 정신질환 환자 수 · {selected_disease} / {selected_gender}")
        st.altair_chart(chart_patient, use_container_width=True)

    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card(col1, f"총 기관 수 ({selected_institution_type})", f"{region_count['기관수'].sum():,}", accent=PRIMARY)
    with col2:
        metric_card(col2, f"환자 수 ({selected_disease} / {selected_gender})", f"{patient_region['환자수'].sum():,.0f}", accent=TEAL)
    with col3:
        metric_card(col3, "평균 인구 10만명당 기관수", f"{merged['인구10만명당기관수'].mean():,.2f}", accent=SLATE)

with tab2:
    section_header("BLIND SPOT RANKING", f"🚨 사각지대 TOP 5 지역 · {selected_institution_type}")

    # 변경: TOP5_COLORS를 디자인 토큰 CORAL 기준 5단계 그라데이션으로 재계산 (하드코딩 색상 제거)
    def _shade(hex_color, factor):
        # hex_color를 흰색 방향으로 factor(0~1)만큼 섞어 밝게 만듦
        h = hex_color.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    TOP5_COLORS = [_shade(CORAL, f) for f in [0.0, 0.18, 0.36, 0.54, 0.72]]
    top5_cols = st.columns(5)
    for rank, (col, (i, row)) in enumerate(zip(top5_cols, top5.iterrows()), start=1):
        with col:
            st.markdown(
                f"""
                <div style="background-color:{TOP5_COLORS[rank-1]}; padding:16px; border-radius:12px; text-align:center;">
                    <div style="font-size:12px; font-weight:700; color:#fff; opacity:0.85; letter-spacing:0.05em;">{rank}위</div>
                    <div style="font-size:18px; font-weight:800; color:#fff; margin:4px 0;">{row['시도']}</div>
                    <div style="font-size:13px; color:#fff;">{row['인구10만명당기관수']:.2f}개 / 10만명</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # 변경: 표 그라데이션도 CORAL 기준 컬러맵으로 통일
    from matplotlib.colors import LinearSegmentedColormap
    coral_cmap = LinearSegmentedColormap.from_list("coral_scale", ["#FBEAE8", CORAL])
    styled_table = (
        merged.drop(columns=["NAME_1"])  # 변경: 지도 매칭용 컬럼이라 표에는 불필요 -> 제거
        .sort_values("인구10만명당기관수", ascending=True)
        .style.background_gradient(subset=["인구10만명당기관수"], cmap=coral_cmap.reversed())
        .format({"인구10만명당기관수": "{:.2f}", "인구수": "{:,.0f}"})
        .hide(axis="index")  # 변경: 인덱스 숫자 컬럼 숨김
    )
    st.dataframe(styled_table, use_container_width=True)

    st.altair_chart(chart_gap, use_container_width=True)

with tab3:
    section_header("GEOGRAPHIC VIEW", f"🗺 사각지대 지도 · {selected_institution_type}")
    st.plotly_chart(fig, use_container_width=True)
