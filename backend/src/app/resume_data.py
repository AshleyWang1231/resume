from app.resume_loader import build_resume_facts

RESUME_FACTS = build_resume_facts()

SUGGESTED_QUESTIONS = {
    "en": [
        "What are Lu's strongest technical areas?",
        "What's the biggest performance win Lu has shipped to production?",
        "How did Lu build an LLM agent reliable enough for a real bank?",
        "How has Lu's work spanned both e-commerce and financial AI?",
    ],
    "zh": [
        "汪露最擅长哪些技术方向？",
        "汪露交付过最大的性能优化是什么？",
        "汪露是怎么让 LLM Agent 在银行生产环境可靠运行的？",
        "汪露的经验是怎么覆盖电商和金融两个领域的？",
    ],
}
