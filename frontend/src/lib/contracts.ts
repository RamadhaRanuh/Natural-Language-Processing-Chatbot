export type Language = "en" | "id";
export interface Passage { id: string; text: string; locator: string }
export interface StudyDatum { label: string; value: string; unit: string | null; passage_id: string; locator: string }
export interface Claim {
  id: string; source_id: string; text: string; display_language: Language;
  verification: "source_extract" | "reviewed_translation";
  passage: Passage; data: StudyDatum[]; data_passages: Passage[];
}
export interface Source {
  id: string; title: string; authors: string[]; year: number; doi: string; pmid: string; pmcid: string;
  url: string; license: string; license_url: string; population: string; design: string;
  limitations: string[]; checked_at: string; document_hash: string;
  copyright_notice: string; adaptation_notice: string;
}
export interface Answer {
  id: string; status: "ready" | "insufficient_evidence" | "blocked_by_scope" | "safety" | "review_required";
  language: Language; message: string; claims: Claim[]; sources: Source[]; notices: string[];
  questions: string[]; research_preview: boolean; safety_url: string | null;
}
