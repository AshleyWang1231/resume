from app.resume_loader import build_resume_facts

RESUME_FACTS = build_resume_facts()

SUGGESTED_QUESTIONS = {
    "en": [
        "How did Lu cut TTFT by 25% at Zalando?",
        "What's the Agent Runtime architecture Lu built?",
        "How does Lu prevent LLM output from being unreliable in production?",
        "What made Lu's Text2SQL agent accurate enough for a real bank?",
    ],
    "zh": [
        "Zalando 的 TTFT 是怎么降了 25% 的？",
        "汪露设计的 Agent Runtime 架构是什么样的？",
        "汪露如何确保 LLM 输出在生产环境可靠？",
        "Text2SQL Agent 是怎么做到银行级准确率的？",
    ],
}
