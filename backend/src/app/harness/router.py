from __future__ import annotations


def route_intent(message: str) -> str:
    query = message.lower()
    if any(term in query for term in ("interview", "面试", "challenge", "conflict", "why")):
        return "interview_answer"
    if any(term in query for term in ("fit", "match", "jd", "job", "岗位", "匹配")):
        return "role_fit"
    if any(term in query for term in ("metric", "impact", "result", "量化", "指标", "成果")):
        return "impact_metrics"
    if any(term in query for term in ("project", "detail", "项目", "经历")):
        return "project_detail"
    return "experience_lookup"

