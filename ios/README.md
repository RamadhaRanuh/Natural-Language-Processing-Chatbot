# Native iPhone app

On a Mac with Xcode and Homebrew:

~~~sh
brew install xcodegen
cd ios
swift test
xcodegen generate
open SehatEvidence.xcodeproj
~~~

Select the SehatEvidence scheme and an iPhone simulator. Start the backend on the same Mac, then set the in-app development server to http://127.0.0.1:8000. This local HTTP exception applies only to DEBUG builds and localhost. For an actual iPhone, configure your hosted HTTPS backend; localhost on a phone refers to the phone.

The app uses SwiftUI, ephemeral URLSession transport, typed committed answers, source/data sheets and a user-reviewed visit summary. It has no HealthKit entitlement, iCloud persistence, analytics, embedded model credential or patient-record upload. Server settings and conversations are kept in memory. Sharing uses the system share sheet only after the user reviews the summary.

The checked-in XcodeGen definition generates the project reproducibly. Signing is deliberately left to your Apple development account, and CI builds the simulator target with signing disabled. Device testing, App Store submission and clinical/legal approval are separate release steps, not claims made by this repository.
