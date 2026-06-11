import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../constants.dart';
import '../storage/secure_storage.dart';

final apiClientProvider = Provider<ApiClient>((ref) {
  final storage = ref.read(secureStorageProvider);
  return ApiClient(storage);
});

class ApiClient {
  ApiClient(this._storage) {
    _dio = Dio(
      BaseOptions(
        baseUrl: AppConstants.apiBaseUrl,
        connectTimeout: const Duration(seconds: 15),
        receiveTimeout: const Duration(seconds: 30),
        headers: <String, String>{'Accept': 'application/json'},
      ),
    );

    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final token = await _storage.readAccessToken();
          if (token != null && token.isNotEmpty) {
            options.headers['Authorization'] = 'Bearer $token';
          }
          handler.next(options);
        },
        onError: (e, handler) async {
          if (e.response?.statusCode == 401) {
            final refreshed = await _tryRefresh();
            if (refreshed && e.requestOptions.path != '/api/v1/auth/refresh') {
              try {
                final clone = await _dio.fetch(e.requestOptions);
                return handler.resolve(clone);
              } catch (_) {/* fall through */}
            }
          }
          handler.next(e);
        },
      ),
    );
  }

  late final Dio _dio;
  final AppSecureStorage _storage;

  Dio get dio => _dio;

  Future<bool> _tryRefresh() async {
    final refresh = await _storage.readRefreshToken();
    if (refresh == null) return false;
    try {
      final res = await Dio(BaseOptions(baseUrl: AppConstants.apiBaseUrl)).post(
        '/api/v1/auth/refresh',
        data: <String, String>{'refreshToken': refresh},
      );
      final tokens = res.data['tokens'] as Map<String, dynamic>;
      await _storage.writeAccessToken(tokens['accessToken'] as String);
      await _storage.writeRefreshToken(tokens['refreshToken'] as String);
      return true;
    } catch (_) {
      await _storage.clear();
      return false;
    }
  }
}
