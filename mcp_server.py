import sys
import json

class ExecutiveBrief:
    @staticmethod
    def generate(metrics):
        high_risk = []
        growth = []
        for kpi, val in metrics.items():
            trend = val.get("trend", "flat") if isinstance(val, dict) else "flat"
            if "risk" in kpi.lower() or "latency" in kpi.lower() or trend == "down":
                high_risk.append({"kpi": kpi, "data": val})
            else:
                growth.append({"kpi": kpi, "data": val})

        summary = (
            f"Business telemetry demonstrates steady progress across {len(growth)} leading indicators. "
            f"Active mitigation recommended for {len(high_risk)} critical metric areas."
        )

        return {
            "summary": summary,
            "growth_indicators": growth,
            "risk_watchpoints": high_risk,
            "action_items": [
                "Review load allocation across high-latency operational regions",
                "Deploy proactive capacity buffer to protect SLA targets"
            ]
        }

def handle_rpc(request):
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "generate_executive_brief",
                        "description": "Synthesize executive brief from metric status updates.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "metrics": {"type": "object"}
                            },
                            "required": ["metrics"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "generate_executive_brief":
            res = ExecutiveBrief.generate(args.get("metrics", {}))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()
