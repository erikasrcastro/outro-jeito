"""Worker Python F3: duas APIs reais e nenhum relato enviado sem triagem."""
import json
from urllib.parse import urlparse
from workers import WorkerEntrypoint, Response, fetch
from flow_live import explore_live
from egress import validate_egress, audit_egress
from texts import fallback

HEADERS = {"Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store",
           "Referrer-Policy": "no-referrer", "X-Content-Type-Options": "nosniff"}
ALLOWED = {"http://127.0.0.1:5173", "http://localhost:5173"}


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        path = urlparse(request.url).path
        headers = dict(HEADERS)
        origin = request.headers.get("Origin")
        if origin in ALLOWED:
            headers.update({"Access-Control-Allow-Origin": origin, "Vary": "Origin",
                            "Access-Control-Allow-Headers": "Content-Type",
                            "Access-Control-Allow-Methods": "POST, GET, OPTIONS"})
        if request.method == "OPTIONS" and path == "/api/v1/explore":
            return Response(None, status=204, headers=headers)
        key = getattr(self.env, "GROQ_API_KEY", None)
        if request.method == "GET" and path == "/api/v1/health":
            info = {"status": "ok", "phase": "F4", "version": "4.3.3", "groq_configured": bool(key),
                    "apis_connected": False}
            return Response(json.dumps(info), headers=headers)
        if request.method == "POST" and path == "/api/v1/explore":
            try:
                body = await request.text()
                payload = json.loads(body) if len(body) <= 2000 else {}
            except Exception:
                payload = {}
            async def secure_fetch(url, **kwargs):
                provider = validate_egress(url, **kwargs)
                audit_egress(provider, getattr(self.env, "EGRESS_AUDIT", "0") == "1")
                return await fetch(url, **kwargs)
            result = await explore_live(payload, key, secure_fetch)
            return Response(json.dumps(result, ensure_ascii=False), headers=headers)
        body = fallback("invalid")
        body.update(status="not_ready", phase="F3", simulated=False)
        return Response(json.dumps(body, ensure_ascii=False), status=404, headers=headers)
