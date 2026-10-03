import XCTest
@testable import SehatCore

final class ContractTests: XCTestCase {
    func testSnakeCaseAnswerDecodesWithEmptyEvidence() throws {
        let json = """
        {"id":"a","status":"insufficient_evidence","language":"id","message":"Unavailable",
        "claims":[],"sources":[],"notices":[],"questions":[],"research_preview":false,"safety_url":null}
        """
        let answer = try ChatAnswer.decode(Data(json.utf8))
        XCTAssertEqual(answer.status, "insufficient_evidence")
        XCTAssertFalse(answer.researchPreview)
        XCTAssertTrue(answer.claims.isEmpty)
    }

    func testRequestUsesAPIFieldNames() throws {
        let encoder = JSONEncoder()
        encoder.keyEncodingStrategy = .convertToSnakeCase
        let request = ChatRequest(messages: [.init(role: "user", content: "diabetes")],
                                  language: "id", adultUser: true, adultPatient: true)
        let object = try XCTUnwrap(JSONSerialization.jsonObject(with: encoder.encode(request)) as? [String: Any])
        XCTAssertEqual(object["adult_user"] as? Bool, true)
        XCTAssertEqual(object["adult_patient"] as? Bool, true)
        XCTAssertNil(object["adultUser"])
    }

    func testTransportCannotExposeClinicalTextOverPublicHTTP() {
        XCTAssertThrowsError(try EndpointPolicy.validate("http://example.com"))
        XCTAssertThrowsError(try EndpointPolicy.validate("http://192.168.1.2", allowLocalHTTP: true))
        XCTAssertThrowsError(try EndpointPolicy.validate("https://secret@example.com"))
        XCTAssertThrowsError(try EndpointPolicy.validate("file:///tmp/data"))
        XCTAssertThrowsError(try EndpointPolicy.validate("https://example.com/?token=secret"))
        XCTAssertNoThrow(try EndpointPolicy.validate("https://example.com"))
        XCTAssertNoThrow(try EndpointPolicy.validate("http://127.0.0.1:8000", allowLocalHTTP: true))
    }
}
