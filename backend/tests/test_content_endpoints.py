from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_market_signals_endpoint_maps_jd_requirements_to_resume_evidence():
    response = client.get("/api/market-signals")
    assert response.status_code == 200
    data = response.json()
    assert data["title_en"] == "What AI Agent roles are screening for"
    assert len(data["signals"]) >= 6
    ids = {item["id"] for item in data["signals"]}
    assert "agent-orchestration" in ids
    assert "evaluation" in ids
    orchestration = next(item for item in data["signals"] if item["id"] == "agent-orchestration")
    assert "Tool Calling" in orchestration["evidence_en"]
    assert orchestration["proof_project_ids"]


def test_capabilities_endpoint_exposes_senior_capability_signals():
    response = client.get("/api/capabilities")
    assert response.status_code == 200
    data = response.json()
    assert data["title_en"] == "Senior AI engineering capability map"
    assert len(data["capabilities"]) >= 5
    capability_ids = {item["id"] for item in data["capabilities"]}
    assert "runtime-architecture" in capability_ids
    assert "evaluation-systems" in capability_ids
    runtime = next(item for item in data["capabilities"] if item["id"] == "runtime-architecture")
    assert "Streaming" in runtime["evidence_en"]
    assert "agent-runtime" in runtime["proof_project_ids"]
