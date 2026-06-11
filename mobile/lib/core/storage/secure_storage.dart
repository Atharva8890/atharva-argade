import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final secureStorageProvider = Provider<AppSecureStorage>((ref) => AppSecureStorage());

class AppSecureStorage {
  AppSecureStorage()
      : _storage = const FlutterSecureStorage(
          aOptions: AndroidOptions(encryptedSharedPreferences: true),
          iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
        );

  final FlutterSecureStorage _storage;

  static const _accessKey = 'vb_access_token';
  static const _refreshKey = 'vb_refresh_token';
  static const _userKey = 'vb_user_json';

  Future<void> writeAccessToken(String token) => _storage.write(key: _accessKey, value: token);
  Future<String?> readAccessToken() => _storage.read(key: _accessKey);
  Future<void> writeRefreshToken(String token) => _storage.write(key: _refreshKey, value: token);
  Future<String?> readRefreshToken() => _storage.read(key: _refreshKey);

  Future<void> writeUser(String json) => _storage.write(key: _userKey, value: json);
  Future<String?> readUser() => _storage.read(key: _userKey);

  Future<void> clear() => _storage.deleteAll();
}
