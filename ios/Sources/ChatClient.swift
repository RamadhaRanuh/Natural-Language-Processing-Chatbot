import Foundation
import SehatCore

enum ChatClientError: LocalizedError {
    case unavailable
    var errorDescription: String? { "The evidence service could not answer. No medical finding was published." }
}

struct ChatClient {
    func ask(_ request: ChatRequest, endpoint: String) async throws -> ChatAnswer {
        #if DEBUG
        let base = try EndpointPolicy.validate(endpoint, allowLocalHTTP: true)
        #else
        let base = try EndpointPolicy.validate(endpoint)
        #endif
        var urlRequest = URLRequest(url: base.appendingPathComponent("v1/chat"))
        urlRequest.httpMethod = "POST"
        urlRequest.setValue("application/json", forHTTPHeaderField: "Content-Type")
        urlRequest.timeoutInterval = 45
        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        urlRequest.httpBody = try encoder.encode(request)
        let configuration = URLSessionConfiguration.ephemeral
        configuration.urlCache = nil
        configuration.requestCachePolicy = .reloadIgnoringLocalCacheData
        let session = URLSession(configuration: configuration, delegate: NoRedirects(), delegateQueue: nil)
        defer { session.invalidateAndCancel() }
        let (data, response) = try await session.data(for: urlRequest)
        guard let http = response as? HTTPURLResponse, http.statusCode == 200 else { throw ChatClientError.unavailable }
        return try ChatAnswer.decode(data)
    }
}

// Never forward conversation bodies to a redirected destination.
private final class NoRedirects: NSObject, URLSessionTaskDelegate {
    func urlSession(_ session: URLSession, task: URLSessionTask,
                    willPerformHTTPRedirection response: HTTPURLResponse,
                    newRequest request: URLRequest,
                    completionHandler: @escaping (URLRequest?) -> Void) {
        completionHandler(nil)
    }
}
