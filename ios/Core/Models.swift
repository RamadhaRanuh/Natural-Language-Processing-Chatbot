import Foundation

public struct ChatMessage: Codable, Sendable {
    public let role: String
    public let content: String
    public init(role: String, content: String) { self.role = role; self.content = content }
}

public struct ChatRequest: Encodable, Sendable {
    public let messages: [ChatMessage]
    public let language: String
    public let adultUser: Bool
    public let adultPatient: Bool
    public init(messages: [ChatMessage], language: String, adultUser: Bool, adultPatient: Bool) {
        self.messages = messages; self.language = language
        self.adultUser = adultUser; self.adultPatient = adultPatient
    }
}

public struct Passage: Decodable, Sendable, Identifiable {
    public let id: String
    public let text: String
    public let locator: String
}

public struct StudyDatum: Decodable, Sendable, Identifiable {
    public var id: String { label + passageId }
    public let label: String
    public let value: String
    public let unit: String?
    public let passageId: String
    public let locator: String
}

public struct Claim: Decodable, Sendable, Identifiable {
    public let id: String
    public let sourceId: String
    public let text: String
    public let displayLanguage: String
    public let verification: String
    public let passage: Passage
    public let data: [StudyDatum]
    public let dataPassages: [Passage]
}

public struct EvidenceSource: Decodable, Sendable, Identifiable {
    public let id: String
    public let title: String
    public let authors: [String]
    public let year: Int
    public let doi: String
    public let pmid: String
    public let pmcid: String
    public let url: String
    public let license: String
    public let population: String
    public let design: String
    public let limitations: [String]
    public let checkedAt: String
    public let copyrightNotice: String
    public let adaptationNotice: String
}

public struct ChatAnswer: Decodable, Sendable, Identifiable {
    public let id: String
    public let status: String
    public let language: String
    public let message: String
    public let claims: [Claim]
    public let sources: [EvidenceSource]
    public let notices: [String]
    public let questions: [String]
    public let researchPreview: Bool
    public let safetyUrl: String?

    public static func decode(_ data: Data) throws -> ChatAnswer {
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try decoder.decode(ChatAnswer.self, from: data)
    }
}

public enum EndpointError: Error { case invalidURL, insecureTransport, credentialsInURL }

public enum EndpointPolicy {
    public static func validate(_ value: String, allowLocalHTTP: Bool = false) throws -> URL {
        guard let url = URL(string: value), let host = url.host, !host.isEmpty,
              url.query == nil, url.fragment == nil else { throw EndpointError.invalidURL }
        guard url.user == nil && url.password == nil else { throw EndpointError.credentialsInURL }
        let local = ["localhost", "127.0.0.1", "::1"].contains(host)
        guard url.scheme == "https" || (allowLocalHTTP && local && url.scheme == "http")
        else { throw EndpointError.insecureTransport }
        return url
    }
}
