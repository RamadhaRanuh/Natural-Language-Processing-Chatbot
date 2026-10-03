"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import type { Answer, Claim, Language, Source } from "@/lib/contracts";

const copy = {
  en: {
    brand: "sehat", evidence: "evidence", about: "Adult diabetes · Research pilot",
    visit: "Prepare for a visit", reset: "New conversation", eyebrow: "UNDERSTANDING STARTS WITH EVIDENCE",
    headline: "A little clarity.\nA better conversation.",
    intro: "Explore diabetes research, see where each finding comes from, and bring better questions to your doctor.",
    age: "I am 18 or older, and the patient is 18 or older.",
    hint: "Your conversation stays in this session. No account or health-record connection.",
    ask: "Ask about adult type 2 diabetes research…", send: "Ask", loading: "Finding studies and checking their sources…",
    suggestions: ["What did diabetes education studies find?", "What does telemonitoring research show?", "What evidence is there about lifestyle?"],
    labels: ["Education & support", "Monitoring research", "Lifestyle evidence"],
    inspect: "Inspect evidence", source: "Source excerpt", study: "The study behind this finding",
    data: "Reported study data", population: "Population", design: "Study design", limitations: "What this study cannot tell us",
    original: "Original passage", dataOriginal: "Data provenance", checked: "Source checked", read: "Read original paper",
    close: "Close", safety: "Official help information", error: "The evidence service is unavailable. Your question has not been answered. Please try again.",
    preview: "Development pilot · Not clinically validated", empty: "Every finding has a source you can inspect.",
    scope: "Education and visit preparation. Personal diagnosis, treatment changes, pediatric and pregnancy advice are outside this pilot.",
    visitTitle: "Your words, ready for your doctor",
    visitIntro: "Record what you want to discuss. This summary organizes your entries; it does not infer a diagnosis.",
    fields: ["Symptoms I want to discuss", "When they started / timing", "My concerns", "Current prescribed medicines (as reported)", "Questions for my doctor"],
    reviewed: "I have reviewed and corrected this summary.",
    copy: "Copy reviewed summary", copied: "Copied", clipboardError: "Clipboard unavailable. Select and copy the preview below.",
    patient: "Patient-reported visit summary", unavailable: "Not reported", translate: "Original English — reviewed Indonesian translation unavailable",
    question: "Questions to bring to your clinician",
  },
  id: {
    brand: "sehat", evidence: "evidence", about: "Diabetes dewasa · Pilot penelitian",
    visit: "Siapkan kunjungan", reset: "Percakapan baru", eyebrow: "MEMAHAMI DIMULAI DARI BUKTI",
    headline: "Lebih jelas.\nLebih siap berdiskusi.",
    intro: "Jelajahi penelitian diabetes, lihat sumber setiap temuan, dan siapkan pertanyaan untuk dokter.",
    age: "Saya dan pasien yang dibahas berusia 18 tahun atau lebih.",
    hint: "Percakapan hanya ada dalam sesi ini. Tanpa akun atau koneksi rekam medis.",
    ask: "Tanyakan penelitian diabetes tipe 2 dewasa…", send: "Tanya", loading: "Mencari penelitian dan memeriksa sumber…",
    suggestions: ["Apa hasil penelitian edukasi diabetes?", "Apa hasil penelitian pemantauan diabetes?", "Apa bukti tentang gaya hidup?"],
    labels: ["Edukasi & dukungan", "Penelitian pemantauan", "Bukti gaya hidup"],
    inspect: "Lihat bukti", source: "Kutipan sumber", study: "Penelitian di balik temuan ini",
    data: "Data yang dilaporkan", population: "Populasi", design: "Desain penelitian", limitations: "Batasan penelitian ini",
    original: "Kutipan asli", dataOriginal: "Asal data", checked: "Sumber diperiksa", read: "Baca penelitian asli",
    close: "Tutup", safety: "Informasi bantuan resmi", error: "Layanan bukti tidak tersedia. Pertanyaan Anda belum dijawab. Silakan coba lagi.",
    preview: "Pilot pengembangan · Belum divalidasi klinis", empty: "Setiap temuan memiliki sumber yang dapat Anda periksa.",
    scope: "Edukasi dan persiapan kunjungan. Diagnosis pribadi, perubahan pengobatan, serta saran anak dan kehamilan di luar cakupan pilot.",
    visitTitle: "Cerita Anda, siap untuk dokter",
    visitIntro: "Catat yang ingin Anda diskusikan. Ringkasan ini menyusun masukan Anda, tanpa menyimpulkan diagnosis.",
    fields: ["Gejala yang ingin saya diskusikan", "Waktu mulai / pola waktu", "Kekhawatiran saya", "Obat yang diresepkan saat ini (sesuai laporan)", "Pertanyaan untuk dokter"],
    reviewed: "Saya sudah meninjau dan mengoreksi ringkasan ini.",
    copy: "Salin ringkasan yang ditinjau", copied: "Disalin", clipboardError: "Papan klip tidak tersedia. Pilih dan salin pratinjau di bawah.",
    patient: "Ringkasan kunjungan sesuai laporan pasien", unavailable: "Tidak dilaporkan", translate: "Bahasa Inggris asli — terjemahan Indonesia yang ditinjau belum tersedia",
    question: "Pertanyaan untuk dokter",
  },
};

type Entry = { question: string; answer?: Answer; error?: boolean };

function Sheet({ title, onClose, children }: { title: string; onClose: () => void; children: React.ReactNode }) {
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const element = dialog.current;
    element?.showModal();
    return () => element?.close();
  }, []);
  return <dialog ref={dialog} className="sheet" aria-label={title} onCancel={onClose}>
    <div className="sheet-head"><h2>{title}</h2><button onClick={onClose} aria-label="Close / Tutup" className="icon-button">×</button></div>
    <div className="sheet-body">{children}</div>
  </dialog>;
}

export default function Home() {
  const [language, setLanguage] = useState<Language>("en");
  const t = copy[language];
  const [adult, setAdult] = useState(false);
  const [query, setQuery] = useState("");
  const [entries, setEntries] = useState<Entry[]>([]);
  const [busy, setBusy] = useState(false);
  const [selected, setSelected] = useState<{ claim: Claim; source: Source } | null>(null);
  const [visit, setVisit] = useState(false);
  const [fields, setFields] = useState(["", "", "", "", ""]);
  const [reviewed, setReviewed] = useState(false);
  const [clipboard, setClipboard] = useState("");
  const abort = useRef<AbortController | null>(null);
  const end = useRef<HTMLDivElement>(null);

  useEffect(() => { document.documentElement.lang = language; }, [language]);
  useEffect(() => { end.current?.scrollIntoView({ behavior: "smooth", block: "nearest" }); }, [entries, busy]);
  useEffect(() => () => abort.current?.abort(), []);

  const summary = t.patient + "\n\n" + fields.map((value, i) => t.fields[i] + ":\n" + (value || t.unavailable)).join("\n\n");

  async function submit(text: string) {
    if (!adult || busy || !text.trim()) return;
    const clean = text.trim().slice(0, 4000);
    const index = entries.length;
    const history = entries.filter((entry) => entry.answer && !entry.error).slice(-4).flatMap((entry) => [
      { role: "user", content: entry.question }, { role: "assistant", content: entry.answer!.message },
    ]);
    const messages = [...history, { role: "user", content: clean }];
    // Match the API's combined 12k-character budget even after long prior turns.
    while (messages.length > 1 && messages.reduce((n, message) => n + message.content.length, 0) > 12000) messages.splice(0, 2);
    setEntries((old) => [...old, { question: clean }]);
    setQuery(""); setBusy(true);
    const controller = new AbortController();
    abort.current = controller;
    try {
      const response = await fetch("/api/chat", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages, language, adult_user: adult, adult_patient: adult }),
        signal: controller.signal,
      });
      if (!response.ok) throw new Error("Unavailable");
      const answer = await response.json() as Answer;
      setEntries((old) => old.map((entry, i) => i === index ? { ...entry, answer } : entry));
    } catch {
      if (!controller.signal.aborted) setEntries((old) => old.map((entry, i) => i === index ? { ...entry, error: true } : entry));
    } finally {
      if (abort.current === controller) { setBusy(false); abort.current = null; }
    }
  }

  function reset() {
    abort.current?.abort(); abort.current = null;
    setEntries([]); setQuery(""); setBusy(false); setSelected(null); setVisit(false);
    setFields(["", "", "", "", ""]); setReviewed(false); setClipboard("");
  }

  async function copySummary() {
    try { await navigator.clipboard.writeText(summary); setClipboard(t.copied); }
    catch { setClipboard(t.clipboardError); }
  }

  return <div className="app">
    <header className="topbar">
      <Link href="/" className="wordmark" aria-label="Sehat Evidence"><span className="mark">✳</span>sehat<span className="wordmark-light">evidence</span></Link>
      <nav aria-label="Main">
        <div className="language" aria-label="Language"><button aria-pressed={language === "en"} onClick={() => setLanguage("en")}>EN</button><button aria-pressed={language === "id"} onClick={() => setLanguage("id")}>ID</button></div>
        <button className="visit-button" onClick={() => setVisit(true)}>{t.visit}<span aria-hidden="true">↗</span></button>
      </nav>
    </header>
    <main>
      <div className="context-row"><span className="context-pill"><span className="dot" />{t.about}</span><button className="text-button" onClick={reset}>＋ {t.reset}</button></div>
      {!entries.length && <section className="hero">
        <div className="hero-symbol" aria-hidden="true">✳</div>
        <p className="eyebrow">{t.eyebrow}</p><h1>{t.headline}</h1><p className="intro">{t.intro}</p>
        <div className="trust-line"><span aria-hidden="true">◈</span>{t.empty}</div>
        <div className="suggestions">{t.suggestions.map((suggestion, i) => <button key={suggestion} disabled={!adult || busy} onClick={() => submit(suggestion)}>
          <span className="suggestion-label">{String(i + 1).padStart(2, "0")} / {t.labels[i]}</span><span>{suggestion}</span><span className="arrow" aria-hidden="true">↗</span>
        </button>)}</div>
      </section>}
      <section className="conversation" aria-live="polite" aria-label={language === "en" ? "Conversation" : "Percakapan"}>
        {entries.map((entry, i) => <article key={i} className="turn">
          <p className="user-question">{entry.question}</p>
          {entry.error ? <div className="notice error" role="alert">{t.error}</div> : entry.answer && <div className="answer">
            <div className="answer-heading"><span className="mark small">✳</span><strong>Sehat Evidence</strong><span className="status-tag">{entry.answer.status.replaceAll("_", " ")}</span></div>
            <p>{entry.answer.message}</p>
            {entry.answer.claims.map((claim) => {
              const source = entry.answer!.sources.find((s) => s.id === claim.source_id);
              return source && <div className="finding" key={claim.id}>
                <p className="finding-label">{t.source} · {source.year}</p>
                <blockquote lang={claim.display_language}>{claim.text}</blockquote>
                {language === "id" && claim.display_language === "en" && <small>{t.translate}</small>}
                <button className="evidence-button" onClick={() => setSelected({ claim, source })}><span>↳ {t.inspect}</span><span>{source.authors[0] || source.pmid} · {claim.data.length} {language === "en" ? "data fields" : "kolom data"} ↗</span></button>
              </div>;
            })}
            {entry.answer.notices.map((notice) => <p className="notice" key={notice}>{notice}</p>)}
            {!!entry.answer.questions.length && <div className="doctor-questions"><h3>{t.question}</h3>{entry.answer.questions.map((question) => <p key={question}>{question}</p>)}</div>}
            {entry.answer.safety_url && <a className="external-link" href={entry.answer.safety_url} target="_blank" rel="noreferrer">{t.safety} ↗</a>}
          </div>}
        </article>)}
        {busy && <p className="loading" role="status"><span className="pulse" />{t.loading}</p>}
        <div ref={end} />
      </section>
      <section className="composer" aria-label={language === "en" ? "Ask a question" : "Ajukan pertanyaan"}>
        <label className="adult"><input type="checkbox" checked={adult} onChange={(e) => setAdult(e.target.checked)} />{t.age}</label>
        <form onSubmit={(event) => { event.preventDefault(); submit(query); }} className="input-shell">
          <textarea aria-label={t.ask} placeholder={t.ask} value={query} maxLength={4000} rows={2} onChange={(e) => setQuery(e.target.value)} disabled={busy}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submit(query); } }} />
          <button disabled={!adult || busy || !query.trim()} type="submit">{t.send} <span aria-hidden="true">↑</span></button>
        </form>
        <p className="session-hint">{t.hint}</p>
      </section>
      <footer><span>{t.preview}</span><p>{t.scope}</p><a href="https://kemkes.go.id/" target="_blank" rel="noreferrer">{t.safety} ↗</a></footer>
    </main>
    {selected && <Sheet title={t.study} onClose={() => setSelected(null)}>
      <div className="source-meta">{selected.source.design} · {selected.source.year}</div><h3 className="paper-title">{selected.source.title}</h3>
      <p>{selected.source.authors.join(", ")}</p><dl className="study-context"><dt>{t.population}</dt><dd>{selected.source.population}</dd><dt>{t.design}</dt><dd>{selected.source.design}</dd></dl>
      <h3>{t.data}</h3><table><thead><tr><th>{language === "en" ? "Measure" : "Ukuran"}</th><th>{language === "en" ? "Reported value" : "Nilai sumber"}</th></tr></thead><tbody>{selected.claim.data.map((datum) => <tr key={datum.label}><td>{datum.label}</td><td>{datum.value} {datum.unit}</td></tr>)}</tbody></table>
      <h3>{t.original}</h3><blockquote className="source-passage">{selected.claim.passage.text}</blockquote><code className="locator">{selected.claim.passage.locator}</code>
      <details><summary>{t.dataOriginal}</summary>{selected.claim.data_passages.map((passage) => <div key={passage.id}><blockquote className="source-passage">{passage.text}</blockquote><code className="locator">{passage.locator}</code></div>)}</details>
      <h3>{t.limitations}</h3><ul>{selected.source.limitations.map((limit) => <li key={limit}>{limit}</li>)}</ul>
      <p className="source-meta">{t.checked}: {new Date(selected.source.checked_at).toLocaleString(language === "id" ? "id-ID" : "en-GB")}</p>
      <p className="source-meta">DOI {selected.source.doi} · PMID {selected.source.pmid} · {selected.source.license}</p>
      <p className="source-meta">{selected.source.copyright_notice}<br />{selected.source.adaptation_notice}</p>
      <a className="primary-link" href={selected.source.url} target="_blank" rel="noreferrer">{t.read} ↗</a>
    </Sheet>}
    {visit && <Sheet title={t.visitTitle} onClose={() => setVisit(false)}>
      <p>{t.visitIntro}</p>
      {fields.map((value, i) => <label className="visit-field" key={i}>{t.fields[i]}<textarea value={value} maxLength={2000} rows={2} onChange={(event) => { setFields((old) => old.map((x, j) => j === i ? event.target.value : x)); setReviewed(false); setClipboard(""); }} /></label>)}
      <label className="adult"><input type="checkbox" checked={reviewed} onChange={(event) => setReviewed(event.target.checked)} />{t.reviewed}</label>
      <button className="primary-link" disabled={!reviewed} onClick={copySummary}>{t.copy}</button>
      {clipboard && <p role="status">{clipboard}</p>}<details><summary>{language === "en" ? "Preview summary" : "Pratinjau ringkasan"}</summary><pre className="summary-preview">{summary}</pre></details>
    </Sheet>}
  </div>;
}
