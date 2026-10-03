"""No unrestricted generation or streaming routes remain."""
from contextlib import asynccontextmanager
import asyncio
import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .config import Config
from .contracts import ChatRequest, ChatAnswer
from .evidence import EvidenceRepository
from .service import ChatService


def create_app(config: Config | None = None, transport: httpx.AsyncBaseTransport | None = None) -> FastAPI:
    settings = config or Config.from_env()

    @asynccontextmanager
    async def lifespan(app):
        async with httpx.AsyncClient(timeout=15, transport=transport, follow_redirects=False) as client:
            repository = EvidenceRepository(settings, client)
            app.state.repository = repository
            app.state.service = ChatService(settings, repository, client)
            yield

    app = FastAPI(title="Sehat Evidence", version="0.1.0", lifespan=lifespan)
    origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",") if x.strip()]
    app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

    @app.middleware("http")
    async def privacy_limits(request: Request, call_next):
        if request.method == "POST":
            total, pieces = 0, []
            async for chunk in request.stream():
                total += len(chunk)
                if total > settings.max_body_bytes:
                    return JSONResponse({"detail": "Request too large."}, status_code=413)
                pieces.append(chunk)
            request._body = b"".join(pieces)
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response

    @app.get("/health")
    async def health(request: Request):
        repo = request.app.state.repository
        return {
            "status": "ok", "environment": settings.environment, "corpus_version": repo.corpus.version,
            "sources": len(repo.corpus.sources),
            "clinical_release_ready": bool(repo.corpus.sources) and all(repo.approved(s) for s in repo.corpus.sources) and repo.safety_approved(),
            "safety_reviewed": repo.safety_approved(),
            "model_configured": bool(settings.model_url and settings.model_key and settings.model_name),
        }

    @app.post("/v1/chat", response_model=ChatAnswer)
    async def chat(request: Request, body: ChatRequest):
        try:
            async with asyncio.timeout(35):
                return await request.app.state.service.answer(body)
        except TimeoutError:
            from uuid import uuid4
            from .service import TEXT
            return ChatAnswer(id=str(uuid4()), status="insufficient_evidence", language=body.language, message=TEXT[body.language]["missing"])

    return app


app = create_app()
