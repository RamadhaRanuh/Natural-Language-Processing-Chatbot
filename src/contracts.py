"""Typed public contract and operator-controlled source records."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Message(StrictModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(StrictModel):
    messages: list[Message] = Field(min_length=1, max_length=12)
    language: Literal["en", "id"] = "en"
    adult_user: bool
    adult_patient: bool
    use_model: bool = False

    @model_validator(mode="after")
    def last_user(self):
        if self.messages[-1].role != "user":
            raise ValueError("The last message must be a user message.")
        if sum(len(m.content) for m in self.messages) > 12000:
            raise ValueError("Conversation is too long.")
        return self


class Passage(BaseModel):
    id: str
    text: str = Field(min_length=1)
    locator: str


class StudyDatum(BaseModel):
    label: str
    value: str
    unit: str | None = None
    passage_id: str
    locator: str


class CorpusClaim(BaseModel):
    id: str
    topic: Literal["education", "monitoring", "lifestyle"]
    text_en: str
    text_id: str | None = None
    passage_id: str
    data: list[StudyDatum] = Field(default_factory=list)


class Source(BaseModel):
    id: str
    title: str
    authors: list[str]
    year: int
    doi: str
    pmid: str
    pmcid: str
    url: str
    license_url: str
    license: str
    document_hash: str
    kind: Literal["paper", "guideline", "drug_information"] = "paper"
    population: str
    design: str
    limitations: list[str]
    passages: list[Passage]
    claims: list[CorpusClaim]
    publication_status: dict = Field(default_factory=dict)
    copyright_notice: str = ""
    adaptation_notice: str = ""


class Corpus(BaseModel):
    version: str
    sources: list[Source]


class PublishedClaim(StrictModel):
    id: str
    source_id: str
    text: str
    original_language: Literal["en"] = "en"
    display_language: Literal["en", "id"]
    verification: Literal["source_extract", "reviewed_translation"]
    passage: Passage
    data: list[StudyDatum]
    data_passages: list[Passage]


class PublishedSource(StrictModel):
    id: str
    title: str
    authors: list[str]
    year: int
    doi: str
    pmid: str
    pmcid: str
    url: str
    license: str
    license_url: str
    kind: str
    population: str
    design: str
    limitations: list[str]
    checked_at: str
    document_hash: str
    copyright_notice: str
    adaptation_notice: str


class ChatAnswer(StrictModel):
    id: str
    status: Literal["ready", "insufficient_evidence", "blocked_by_scope", "safety", "review_required"]
    language: Literal["en", "id"]
    message: str
    claims: list[PublishedClaim] = Field(default_factory=list)
    sources: list[PublishedSource] = Field(default_factory=list)
    notices: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    topic: str | None = None
    research_preview: bool = False
    safety_url: str | None = None
