class AppConstants {
  AppConstants._();

  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://10.0.2.2:4000',
  );

  static const String socketUrl = String.fromEnvironment(
    'SOCKET_URL',
    defaultValue: 'http://10.0.2.2:4000',
  );

  static const String appName = 'VoiceBridge AI';

  static const List<({String code, String name, String native})> supportedLanguages = [
    (code: 'en', name: 'English', native: 'English'),
    (code: 'hi', name: 'Hindi', native: 'हिन्दी'),
    (code: 'mr', name: 'Marathi', native: 'मराठी'),
    (code: 'gu', name: 'Gujarati', native: 'ગુજરાતી'),
    (code: 'pa', name: 'Punjabi', native: 'ਪੰਜਾਬੀ'),
    (code: 'ta', name: 'Tamil', native: 'தமிழ்'),
    (code: 'te', name: 'Telugu', native: 'తెలుగు'),
    (code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ'),
    (code: 'ml', name: 'Malayalam', native: 'മലയാളം'),
    (code: 'bn', name: 'Bengali', native: 'বাংলা'),
    (code: 'ur', name: 'Urdu', native: 'اُردُو'),
    (code: 'ar', name: 'Arabic', native: 'العربية'),
    (code: 'zh', name: 'Chinese', native: '中文'),
    (code: 'ja', name: 'Japanese', native: '日本語'),
    (code: 'ko', name: 'Korean', native: '한국어'),
    (code: 'fr', name: 'French', native: 'Français'),
    (code: 'de', name: 'German', native: 'Deutsch'),
    (code: 'es', name: 'Spanish', native: 'Español'),
    (code: 'ru', name: 'Russian', native: 'Русский'),
  ];
}
