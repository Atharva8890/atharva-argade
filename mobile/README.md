# VoiceBridge AI - Mobile (Flutter)

Production-ready Flutter app for Android + iOS that pairs with the VoiceBridge AI backend.

## Run

```bash
cd mobile
flutter pub get
flutter run --dart-define=API_BASE_URL=http://10.0.2.2:4000 \
             --dart-define=SOCKET_URL=http://10.0.2.2:4000
```

For a physical device, replace `10.0.2.2` with your machine's LAN IP.

## Layout

```
lib/
├── main.dart                    Bootstraps Flutter + Riverpod
├── app.dart                     MaterialApp + router + theme
├── core/
│   ├── constants.dart           API base URL, supported languages
│   ├── theme/                   Dark theme with electric-blue accents
│   ├── routes/app_router.dart   go_router routes
│   ├── network/                 Dio HTTP client + Socket.io wrapper
│   └── storage/secure_storage.dart   Encrypted token storage
└── features/
    ├── splash/                  Animated splash with auth-aware routing
    ├── auth/                    Login, signup, OTP, forgot password
    ├── home/                    Tabbed shell (Calls / Contacts / Settings)
    ├── contacts/                Contacts list with quick-call buttons
    ├── call/                    Live captions + WebRTC call screen
    ├── transcript/              Scrollable transcript w/ copy/download/share
    ├── subscription/            Free / Premium / Business plan picker
    ├── settings/                Profile, preferences, account
    └── meetings/                AI meeting room entry
```

## Platform setup

Before running you'll need to scaffold the native platform folders (these are not checked in to keep the repo lean):

```bash
flutter create --platforms=android,ios .
```

Then add the following permissions:

**Android (`android/app/src/main/AndroidManifest.xml`):**

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
<uses-permission android:name="android.permission.FOREGROUND_SERVICE_MICROPHONE" />
```

**iOS (`ios/Runner/Info.plist`):**

```xml
<key>NSMicrophoneUsageDescription</key>
<string>VoiceBridge AI uses your microphone to translate your voice in real time.</string>
<key>NSCameraUsageDescription</key>
<string>Optional camera access for video calls.</string>
<key>NSContactsUsageDescription</key>
<string>VoiceBridge AI uses contacts to help you start translated calls.</string>
<key>UIBackgroundModes</key>
<array>
  <string>audio</string>
  <string>voip</string>
</array>
```

Drop the Inter font files into `assets/fonts/` (Inter-Regular, Medium, SemiBold, Bold) or remove the `fonts:` block in `pubspec.yaml` to fall back to Google Fonts.
