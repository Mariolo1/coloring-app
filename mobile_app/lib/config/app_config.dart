import 'dart:io';

class AppConfig {
  static const String _defaultPort = '8001';

  /// Możesz nadpisać backend przez:
  /// flutter run --dart-define=API_BASE_URL=http://192.168.1.50:8000
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: '',
  );

  static String resolveBaseUrl() {
    if (apiBaseUrl.isNotEmpty) {
      return apiBaseUrl;
    }

    if (Platform.isAndroid) {
      return 'http://10.0.2.2:' + _defaultPort;
    }

    // iOS simulator nie używa 10.0.2.2.
    // Dla iPhone'a i iOS simulatora podaj IP komputera przez --dart-define.
    return 'http://127.0.0.1:' + _defaultPort;
  }
}
