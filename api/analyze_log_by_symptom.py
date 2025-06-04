from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/analyze_log_by_symptom")
async def analyze_log_by_symptom(request: Request):
    data = await request.json()
    symptom = data.get("symptom_description", "").lower()
    log_lines = data.get("log_lines", [])

    matched = [line for line in log_lines if any(
        keyword in line.lower() for keyword in ["fatal", "anr", "black", "sigsegv", "reboot", "dropbox"]
    ) or symptom.split()[0] in line.lower()]

    return {
        "insight": f"症状 '{symptom}' に関連しそうなログが {len(matched)} 行見つかりました。",
        "matched_lines": matched[-10:]  # 最新の10件を返す例
    }
