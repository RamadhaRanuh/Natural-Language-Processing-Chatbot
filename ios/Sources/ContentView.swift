import SwiftUI
import SehatCore

private let forest = Color(red: 0.10, green: 0.30, blue: 0.23)

struct EvidenceSelection: Identifiable {
    var id: String { claim.id }
    let claim: Claim
    let source: EvidenceSource
}

struct ContentView: View {
    @State private var language = "en"
    @State private var adult = false
    @State private var question = ""
    @State private var messages: [ChatMessage] = []
    @State private var answers: [(String, ChatAnswer)] = []
    @State private var busy = false
    @State private var error: String?
    @State private var endpoint = ""
    @State private var showSettings = false
    @State private var showVisit = false
    @State private var selected: EvidenceSelection?
    @State private var generation = UUID()

    private func text(_ en: String, _ id: String) -> String { language == "en" ? en : id }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    HStack {
                        Label("Sehat Evidence", systemImage: "leaf")
                            .font(.headline).foregroundStyle(forest)
                        Spacer()
                        Picker("Language / Bahasa", selection: $language) {
                            Text("EN").tag("en"); Text("ID").tag("id")
                        }.pickerStyle(.segmented).frame(width: 110)
                    }
                    Text(text("Adult diabetes · Research pilot", "Diabetes dewasa · Pilot penelitian"))
                        .font(.caption).foregroundStyle(.secondary)
                    if answers.isEmpty {
                        Text(text("A little clarity.\nA better conversation.", "Lebih jelas.\nLebih siap berdiskusi."))
                            .font(.system(.largeTitle, design: .serif)).foregroundStyle(forest)
                        Text(text("Inspect the evidence and prepare questions for your doctor.", "Periksa bukti dan siapkan pertanyaan untuk dokter."))
                            .foregroundStyle(.secondary)
                        ForEach(Array(suggestions.enumerated()), id: \.offset) { _, item in
                            Button { question = item; Task { await send() } } label: {
                                HStack { Text(item); Spacer(); Image(systemName: "arrow.up.right") }
                                    .padding().frame(maxWidth: .infinity, alignment: .leading)
                                    .background(.background).clipShape(RoundedRectangle(cornerRadius: 14))
                            }.disabled(!adult || busy)
                        }
                    }
                    ForEach(Array(answers.enumerated()), id: \.offset) { _, turn in
                        VStack(alignment: .leading, spacing: 12) {
                            Text(turn.0).font(.headline)
                            Text(turn.1.message)
                            ForEach(turn.1.claims) { claim in
                                if let source = turn.1.sources.first(where: { $0.id == claim.sourceId }) {
                                    VStack(alignment: .leading, spacing: 10) {
                                        Text(text("Source excerpt", "Kutipan sumber")).font(.caption).foregroundStyle(.secondary)
                                        Text(claim.text).font(.system(.title3, design: .serif))
                                        if language == "id" && claim.displayLanguage == "en" {
                                            Text("Bahasa Inggris asli — terjemahan yang ditinjau belum tersedia").font(.caption)
                                        }
                                        Button(text("Inspect evidence", "Lihat bukti")) { selected = EvidenceSelection(claim: claim, source: source) }
                                    }.padding().background(.background).clipShape(RoundedRectangle(cornerRadius: 14))
                                }
                            }
                            ForEach(turn.1.notices, id: \.self) { Text($0).font(.caption).foregroundStyle(.secondary) }
                            ForEach(turn.1.questions, id: \.self) { Text($0).font(.callout) }
                            if let link = turn.1.safetyUrl, let url = URL(string: link) {
                                Link(text("Official help information", "Informasi bantuan resmi"), destination: url)
                            }
                        }.padding(.vertical, 8)
                    }
                    if busy { ProgressView(text("Checking evidence…", "Memeriksa bukti…")) }
                    if error != nil { Text(text("Evidence service unavailable. Please check the server setting and try again.", "Layanan bukti tidak tersedia. Periksa pengaturan server dan coba lagi.")).foregroundStyle(.red).accessibilityAddTraits(.updatesFrequently) }
                    Toggle(text("I and the patient are 18 or older.", "Saya dan pasien berusia 18 tahun atau lebih."), isOn: $adult).font(.caption)
                    HStack(alignment: .bottom) {
                        TextField(text("Ask about adult diabetes research", "Tanyakan penelitian diabetes dewasa"), text: $question, axis: .vertical)
                            .lineLimit(2...5).textFieldStyle(.roundedBorder)
                        Button { Task { await send() } } label: { Image(systemName: "arrow.up.circle.fill").font(.title) }
                            .accessibilityLabel(text("Ask", "Tanya")).disabled(!adult || busy || question.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                    }
                    Text(text("Development pilot, not clinically validated. No conversation is saved. Personal diagnosis and treatment changes are outside this pilot.", "Pilot pengembangan, belum divalidasi klinis. Percakapan tidak disimpan. Diagnosis pribadi dan perubahan pengobatan di luar cakupan."))
                        .font(.caption).foregroundStyle(.secondary)
                    Link(text("Official help information", "Informasi bantuan resmi"), destination: URL(string: "https://kemkes.go.id/")!).font(.caption)
                }.padding()
            }.background(Color(red: 0.97, green: 0.98, blue: 0.95))
                .navigationTitle(text("Understand the evidence", "Pahami buktinya")).navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .topBarLeading) {
                        Button { reset() } label: { Image(systemName: "arrow.counterclockwise") }.accessibilityLabel(text("Reset session", "Hapus sesi"))
                    }
                    ToolbarItemGroup(placement: .topBarTrailing) {
                        Button { showVisit = true } label: { Image(systemName: "list.clipboard") }.accessibilityLabel(text("Prepare a visit", "Siapkan kunjungan"))
                        Button { showSettings = true } label: { Image(systemName: "gear") }.accessibilityLabel(text("Server settings", "Pengaturan server"))
                    }
                }
                .sheet(item: $selected) { EvidenceView(selection: $0, language: language) }
                .sheet(isPresented: $showVisit) { VisitView(language: language) }
                .sheet(isPresented: $showSettings) {
                    NavigationStack {
                        Form {
                            TextField("HTTPS API URL", text: $endpoint).textInputAutocapitalization(.never).autocorrectionDisabled().keyboardType(.URL)
                            Text(text("Use an HTTPS service. DEBUG simulator builds also permit localhost HTTP. Endpoint settings stay in memory.", "Gunakan layanan HTTPS. Simulator DEBUG mengizinkan HTTP localhost. Pengaturan hanya ada dalam memori.")).font(.caption)
                        }.navigationTitle(text("Evidence server", "Server bukti"))
                            .toolbar { ToolbarItem(placement: .confirmationAction) { Button(text("Done", "Selesai")) { showSettings = false } } }
                    }
                }
        }.tint(forest)
    }

    private var suggestions: [String] {
        language == "en"
        ? ["What did diabetes education studies find?", "What does telemonitoring research show?", "What evidence is there about lifestyle?"]
        : ["Apa hasil penelitian edukasi diabetes?", "Apa hasil penelitian pemantauan diabetes?", "Apa bukti tentang gaya hidup?"]
    }

    @MainActor private func send() async {
        guard adult, !busy, !question.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else { return }
        let input = String(question.prefix(4000))
        question = ""; busy = true; error = nil
        let token = generation
        var history = Array(messages.suffix(8)) + [ChatMessage(role: "user", content: input)]
        while history.count > 1 && history.reduce(0, { $0 + $1.content.count }) > 12000 { history.removeFirst(2) }
        do {
            let response = try await ChatClient().ask(ChatRequest(messages: history, language: language, adultUser: adult, adultPatient: adult), endpoint: endpoint)
            guard generation == token else { return }
            answers.append((input, response))
            messages = history + [ChatMessage(role: "assistant", content: response.message)]
        } catch {
            guard generation == token else { return }
            self.error = "unavailable"
        }
        if generation == token { busy = false }
    }

    private func reset() {
        generation = UUID(); messages = []; answers = []; question = ""; busy = false; error = nil
        selected = nil; showVisit = false
    }
}

struct EvidenceView: View {
    let selection: EvidenceSelection
    let language: String
    @Environment(\.dismiss) private var dismiss
    private func text(_ en: String, _ id: String) -> String { language == "en" ? en : id }
    var body: some View {
        NavigationStack {
            List {
                Section(text("Study", "Penelitian")) {
                    Text(selection.source.title).font(.headline)
                    Text(selection.source.authors.joined(separator: ", ")).font(.caption)
                    Text(selection.source.population); Text(selection.source.design)
                }
                Section(text("Reported data", "Data yang dilaporkan")) {
                    ForEach(selection.claim.data) { datum in
                        VStack(alignment: .leading) { Text(datum.label).font(.caption); Text(datum.value + " " + (datum.unit ?? "")) }
                    }
                }
                Section(text("Original source passage", "Kutipan sumber asli")) {
                    Text(selection.claim.passage.text).textSelection(.enabled)
                    Text(selection.claim.passage.locator).font(.caption).textSelection(.enabled)
                }
                Section(text("Data provenance", "Asal data")) {
                    ForEach(selection.claim.dataPassages) { passage in
                        VStack(alignment: .leading) { Text(passage.text); Text(passage.locator).font(.caption) }
                    }
                }
                Section(text("Limitations", "Batasan")) {
                    ForEach(selection.source.limitations, id: \.self) { Text($0) }
                }
                Section {
                    Text(selection.source.checkedAt).font(.caption)
                    Text(selection.source.copyrightNotice).font(.caption)
                    Text(selection.source.adaptationNotice).font(.caption)
                    Text(selection.source.license).font(.caption)
                    if let url = URL(string: selection.source.url) { Link(text("Read original paper", "Baca penelitian asli"), destination: url) }
                }
            }.navigationTitle(text("Inspect evidence", "Lihat bukti"))
                .toolbar { ToolbarItem(placement: .confirmationAction) { Button(text("Done", "Selesai")) { dismiss() } } }
        }
    }
}

struct VisitView: View {
    let language: String
    @State private var fields = ["", "", "", "", ""]
    @State private var reviewed = false
    @Environment(\.dismiss) private var dismiss
    private var labels: [String] {
        language == "en" ? ["Symptoms to discuss", "Timing", "Concerns", "Current prescribed medicines (reported)", "Questions for my doctor"]
        : ["Gejala yang ingin didiskusikan", "Waktu mulai / pola waktu", "Kekhawatiran", "Obat yang diresepkan (sesuai laporan)", "Pertanyaan untuk dokter"]
    }
    private var summary: String {
        (language == "en" ? "Patient-reported visit summary" : "Ringkasan sesuai laporan pasien") + "\n\n" +
        zip(labels, fields).map { $0.0 + ":\n" + ($0.1.isEmpty ? "—" : $0.1) }.joined(separator: "\n\n")
    }
    var body: some View {
        NavigationStack {
            Form {
                Text(language == "en" ? "Your entries are organized verbatim. No diagnosis is inferred. Review before sharing." : "Masukan Anda disusun sesuai laporan, tanpa diagnosis. Tinjau sebelum membagikan.").font(.caption)
                ForEach(0..<fields.count, id: \.self) { index in
                    TextField(labels[index], text: $fields[index], axis: .vertical).lineLimit(2...5)
                        .onChange(of: fields[index]) { _, newValue in
                            fields[index] = String(newValue.prefix(2000)); reviewed = false
                        }
                }
                Toggle(language == "en" ? "I reviewed and corrected this summary" : "Saya sudah meninjau dan mengoreksi ringkasan", isOn: $reviewed)
                if reviewed { ShareLink(item: summary) { Label(language == "en" ? "Share reviewed summary" : "Bagikan ringkasan", systemImage: "square.and.arrow.up") } }
                DisclosureGroup(language == "en" ? "Preview" : "Pratinjau") { Text(summary).textSelection(.enabled) }
            }.navigationTitle(language == "en" ? "Prepare your visit" : "Siapkan kunjungan")
                .toolbar { ToolbarItem(placement: .confirmationAction) { Button(language == "en" ? "Done" : "Selesai") { dismiss() } } }
        }
    }
}
