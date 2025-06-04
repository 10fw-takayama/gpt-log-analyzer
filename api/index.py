from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/detect_log_stop_event")
async def detect_log_stop_event(request: Request):
    body = await request.json()
    log_lines = body.get("log_lines", [])

    for line in reversed(log_lines):
        if "日志工具已停止" in line or "log tool stopped" in line:
            return {"stopped": True, "reason": line.strip()}
    return {"stopped": False, "reason": "Log output continues normally."}


@app.post("/analyze_log_by_symptom")
async def analyze_log_by_symptom(request: Request):
    data = await request.json()
    symptom = data.get("symptom_description", "").lower()
    log_lines = data.get("log_lines", [])

    # 簡易マッチロジック（今後強化可能）
    keywords = ["fatal", "anr", "sigsegv", "reboot", "black", "error", "dropbox"]
    matched = [
        line for line in log_lines
        if any(k in line.lower() for k in keywords) or symptom in line.lower()
    ]

    return {
        "insight": f"症状 '{symptom}' に関連しそうなログが {len(matched)} 行見つかりました。",
        "matched_lines": matched[-10:]  # 最後の10件を返す例
    }
