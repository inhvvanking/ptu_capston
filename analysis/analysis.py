
import pandas as pd
import plotly.graph_objects as go

DATA_PATH = "data/survey.csv"

behavior_cols = [
    "평소 분리수거(재활용)를 얼마나 자주 실천하시나요?",
    "평소 자가용 대신 대중교통을 사용하는 빈도는 얼마나 되나요?",
    "평소 텀블러 혹은 개인 다회용 컵을 사용하는 빈도는 얼마나 되나요?",
    "배달 주문 시 일회용품 사용을 거부하는 빈도는 얼마나 되나요?",
    "음식물/폐기물 줄이기를 실천하는 빈도는 얼마나 되나요?"
]

def _stats(df):
    return df[behavior_cols].mean()

def _filters(df):
    grades = sorted(df["귀하의 학년은?"].dropna().unique())
    majors = sorted(df["귀하의 전공계열은?"].dropna().unique())
    return grades, majors

def _interpret(avg):
    if avg >= 4:
        return "전반적으로 친환경 행동 실천 수준이 매우 높은 편입니다."
    elif avg >= 3:
        return "친환경 인식에 비해 실천 수준은 보통 수준으로, 일부 행동에서 개선 여지가 있습니다."
    else:
        return "전반적인 친환경 행동 실천 수준이 낮아 캠퍼스 차원의 개입이 필요합니다."

def analyze():
    df = pd.read_csv(DATA_PATH)
    means = _stats(df)
    grades, majors = _filters(df)
    avg = means.mean()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=means.index, y=means.values, mode="lines+markers", name="현재"))

    return {
        "graph": fig.to_html(full_html=False),
        "avg": round(avg, 2),
        "summary": None,
        "lowest_action": means.idxmin(),
        "interpretation": _interpret(avg),
        "grades": grades,
        "majors": majors
    }

def simulate(action):
    df = pd.read_csv(DATA_PATH)
    before = _stats(df)
    before_avg = before.mean()

    if action == "tumbler":
        df["평소 텀블러 혹은 개인 다회용 컵을 사용하는 빈도는 얼마나 되나요?"] += 1
    elif action == "transport":
        df["평소 자가용 대신 대중교통을 사용하는 빈도는 얼마나 되나요?"] += 1
    elif action == "disposable":
        df["배달 주문 시 일회용품 사용을 거부하는 빈도는 얼마나 되나요?"] += 1
    elif action == "campaign":
        for c in behavior_cols:
            df[c] += 0.5

    for c in behavior_cols:
        df[c] = df[c].clip(upper=5)

    after = _stats(df)
    after_avg = after.mean()
    grades, majors = _filters(df)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=before.index, y=before.values, mode="lines+markers", name="현재"))
    fig.add_trace(go.Scatter(x=after.index, y=after.values, mode="lines+markers", name="시뮬레이션 후"))

    return {
        "graph": fig.to_html(full_html=False),
        "avg": round(after_avg, 2),
        "summary": {
            "before": round(before_avg, 2),
            "after": round(after_avg, 2),
            "diff": round(after_avg - before_avg, 2)
        },
        "lowest_action": after.idxmin(),
        "interpretation": _interpret(after_avg),
        "grades": grades,
        "majors": majors
    }

def analyze_filtered(grade=None, major=None):
    df = pd.read_csv(DATA_PATH)
    full = df.copy()

    if grade:
        df = df[df["귀하의 학년은?"] == grade]
    if major:
        df = df[df["귀하의 전공계열은?"] == major]

    means = _stats(df)
    avg = means.mean()
    grades, majors = _filters(full)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=means.index, y=means.values, mode="lines+markers", name="필터 결과"))

    return {
        "graph": fig.to_html(full_html=False),
        "avg": round(avg, 2),
        "summary": None,
        "lowest_action": means.idxmin(),
        "interpretation": _interpret(avg),
        "grades": grades,
        "majors": majors
    }
