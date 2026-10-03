import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const upstream = process.env.EVIDENCE_API_URL || "http://127.0.0.1:8000";
  let endpoint: URL;
  try {
    endpoint = new URL(upstream);
    if (endpoint.username || endpoint.password || endpoint.search || endpoint.hash) throw new Error("Invalid endpoint");
    if (endpoint.protocol !== "https:" && !(endpoint.protocol === "http:" && ["localhost", "127.0.0.1"].includes(endpoint.hostname))) {
      throw new Error("Invalid transport");
    }
  } catch {
    return NextResponse.json({ detail: "Backend configuration is unavailable." }, { status: 503 });
  }
  try {
    const reader = request.body?.getReader();
    if (!reader) return NextResponse.json({ detail: "Request is empty." }, { status: 400 });
    const chunks: Uint8Array[] = [];
    let size = 0;
    while (true) {
      const part = await reader.read();
      if (part.done) break;
      size += part.value.length;
      if (size > 32768) {
        await reader.cancel();
        return NextResponse.json({ detail: "Request too large." }, { status: 413 });
      }
      chunks.push(part.value);
    }
    const body = Buffer.concat(chunks.map((chunk) => Buffer.from(chunk))).toString("utf8");
    JSON.parse(body);
    const response = await fetch(new URL("/v1/chat", endpoint), {
      method: "POST", headers: { "Content-Type": "application/json" },
      body, cache: "no-store", redirect: "error", signal: AbortSignal.timeout(45000),
    });
    if (!response.ok) return NextResponse.json({ detail: "The request could not be processed." }, { status: response.status });
    return NextResponse.json(await response.json(), { headers: { "Cache-Control": "no-store" } });
  } catch {
    return NextResponse.json({ detail: "Evidence service unavailable. Please try again." }, { status: 503, headers: { "Cache-Control": "no-store" } });
  }
}
