# api/index.py
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
