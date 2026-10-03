// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "SehatCore",
    platforms: [.iOS(.v17), .macOS(.v13)],
    products: [.library(name: "SehatCore", targets: ["SehatCore"])],
    targets: [
        .target(name: "SehatCore", path: "Core"),
        .testTarget(name: "SehatCoreTests", dependencies: ["SehatCore"], path: "Tests"),
    ]
)
