"""Publish a typed answer only after complete source/claim checks."""
import re
from uuid import uuid4
import httpx
from .config import Config
from .contracts import ChatRequest, ChatAnswer, PublishedSource
from .evidence import EvidenceRepository, EvidenceUnavailable
from .model import select_claims, SelectionError
from .safety import guard, SAFETY_URL
from .verification import verify_claim, VerificationError

TEXT = {
    "en": {
        "adult": "This pilot is for users and patients aged 18 or older.",
        "scope": "I can help with general adult type 2 diabetes evidence and questions for your clinician. I cannot diagnose, set personal targets or change treatment.",
        "safety": "This app cannot assess emergencies. If you believe you need immediate help, contact local emergency services. Do not wait for a chat answer.",
        "missing": "I cannot publish a supported finding for this question. The corpus may not cover it, or current source checks could not be completed.",
        "review": "Patient release is awaiting clinical review. No medical findings have been published.",
        "ready": "These are findings from the cited studies. Tap each finding to inspect its original passage and reported data.",
        "preview": "Development research preview: source support is checked; clinical suitability has not been approved.",
        "english": "Research extracts remain in original English. Unreviewed Indonesian medical translations are withheld.",
        "limit": "Source support does not establish medical certainty or applicability to your situation.",
        "question": "What questions should I bring to my clinician about this evidence?",
    },
    "id": {
        "adult": "Pilot ini untuk pengguna dan pasien berusia 18 tahun atau lebih.",
        "scope": "Saya dapat membantu menjelaskan bukti umum diabetes tipe 2 dewasa dan menyusun pertanyaan untuk dokter. Saya tidak dapat mendiagnosis, menetapkan target pribadi, atau mengubah pengobatan.",
        "safety": "Aplikasi ini tidak dapat menilai keadaan darurat. Jika Anda merasa membutuhkan bantuan segera, hubungi layanan darurat setempat. Jangan menunggu jawaban chatbot.",
        "missing": "Saya tidak dapat menampilkan temuan yang didukung sumber untuk pertanyaan ini. Korpus mungkin belum mencakupnya, atau pemeriksaan sumber terkini belum dapat diselesaikan.",
        "review": "Penggunaan oleh pasien masih menunggu tinjauan klinis. Tidak ada temuan medis yang ditampilkan.",
        "ready": "Berikut temuan dari penelitian yang dirujuk. Ketuk setiap temuan untuk melihat kutipan asli dan data yang dilaporkan.",
        "preview": "Pratinjau penelitian untuk pengembangan: dukungan sumber diperiksa; kelayakan klinis belum disetujui.",
        "english": "Kutipan penelitian tetap dalam bahasa Inggris asli. Terjemahan medis Indonesia yang belum ditinjau tidak ditampilkan.",
        "limit": "Dukungan sumber tidak membuktikan kepastian medis atau kesesuaian dengan kondisi Anda.",
        "question": "Apa yang perlu saya tanyakan kepada dokter tentang bukti ini?",
    },
}


def topic_for(text: str) -> str | None:
    topics = {
        "monitoring": r"\b(monitor\w*|telemonitor\w*|pemantauan|pantau|hba1c|a1c)\b",
        "lifestyle": r"\b(lifestyle|diet|exercise|gaya hidup|makan|olahraga)\b",
        "education": r"\b(diabet\w*|type 2|tipe 2|t2d|education|edukasi)\b",
    }
    return next((topic for topic, pattern in topics.items() if re.search(pattern, text, re.I)), None)


class ChatService:
    def __init__(self, config: Config, repository: EvidenceRepository, client: httpx.AsyncClient):
        self.config, self.repository, self.client = config, repository, client

    async def answer(self, request: ChatRequest) -> ChatAnswer:
        text = TEXT[request.language]
        answer = ChatAnswer(id=str(uuid4()), status="insufficient_evidence", language=request.language, message=text["missing"])
        user_text = "\n".join(m.content for m in request.messages if m.role == "user")
        boundary = guard(user_text)
        if boundary == "safety":
            answer.status, answer.message, answer.safety_url = "safety", text["safety"], SAFETY_URL
            return answer
        if not request.adult_user or not request.adult_patient:
            answer.status, answer.message = "blocked_by_scope", text["adult"]
            return answer
        if boundary:
            answer.status, answer.message = boundary, text["safety" if boundary == "safety" else "scope"]
            answer.safety_url = SAFETY_URL if boundary == "safety" else None
            answer.questions = [] if boundary == "safety" else [text["question"]]
            return answer
        topic = topic_for(request.messages[-1].content)
        if topic is None and re.fullmatch(r"\s*(tell me more|what about the results|jelaskan lebih lanjut|bagaimana hasilnya)[?.! ]*\s*", request.messages[-1].content.lower()):
            topic = next((topic_for(m.content) for m in reversed(request.messages[:-1]) if m.role == "user" and topic_for(m.content)), None)
        if topic is None:
            answer.status, answer.message = "blocked_by_scope", text["scope"]
            return answer
        answer.topic = topic
        candidates = [(s, c) for s in self.repository.corpus.sources for c in s.claims if c.topic == topic]
        if not candidates:
            return answer
        if self.config.environment == "production" and not self.repository.safety_approved():
            answer.status, answer.message = "review_required", text["review"]
            return answer
        if request.use_model:
            try:
                chosen = await select_claims(topic, [c.id for _, c in candidates], self.config, self.client)
                candidates = [(s, c) for s, c in candidates if c.id in chosen]
            except SelectionError:
                return answer
        published, sources = [], {}
        for source, claim in candidates[:4]:
            if self.config.environment == "production" and not self.repository.approved(source):
                continue
            try:
                check = await self.repository.check(source)
                verified = verify_claim(source, claim, request.language, self.repository.reviews)
                published.append(verified)
                sources[source.id] = PublishedSource(
                    **source.model_dump(exclude={"passages", "claims", "publication_status"}),
                    checked_at=check.checked_at,
                )
            except (EvidenceUnavailable, VerificationError):
                continue
        if not published:
            if self.config.environment == "production" and not any(self.repository.approved(s) for s, _ in candidates):
                answer.status, answer.message = "review_required", text["review"]
            return answer
        answer.status, answer.message = "ready", text["ready"]
        answer.claims, answer.sources = published, list(sources.values())
        answer.questions, answer.notices = [text["question"]], [text["limit"]]
        answer.research_preview = self.config.environment != "production"
        if answer.research_preview:
            answer.notices.insert(0, text["preview"])
        if request.language == "id" and any(c.display_language == "en" for c in published):
            answer.notices.append(text["english"])
        return answer
