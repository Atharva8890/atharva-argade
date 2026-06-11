import 'dart:async';

import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/auth_repository.dart';

class AuthState {
  const AuthState({this.user, this.loading = false, this.error});

  final Map<String, dynamic>? user;
  final bool loading;
  final String? error;

  bool get isAuthenticated => user != null;

  AuthState copyWith({Map<String, dynamic>? user, bool? loading, String? error, bool clearError = false}) {
    return AuthState(
      user: user ?? this.user,
      loading: loading ?? this.loading,
      error: clearError ? null : (error ?? this.error),
    );
  }
}

class AuthController extends StateNotifier<AuthState> {
  AuthController(this._repo) : super(const AuthState()) {
    _bootstrap();
  }

  final AuthRepository _repo;

  Future<void> _bootstrap() async {
    final cached = await _repo.currentUser();
    if (cached != null) {
      state = state.copyWith(user: cached);
    }
  }

  Future<void> login(String email, String password) async {
    state = state.copyWith(loading: true, clearError: true);
    try {
      final res = await _repo.login(email: email, password: password);
      state = state.copyWith(user: res['user'] as Map<String, dynamic>, loading: false);
    } catch (e) {
      state = state.copyWith(loading: false, error: e.toString());
    }
  }

  Future<void> signup({
    required String name,
    required String email,
    required String password,
    String language = 'en',
    String? phone,
  }) async {
    state = state.copyWith(loading: true, clearError: true);
    try {
      final res = await _repo.signup(name: name, email: email, password: password, language: language, phone: phone);
      state = state.copyWith(user: res['user'] as Map<String, dynamic>, loading: false);
    } catch (e) {
      state = state.copyWith(loading: false, error: e.toString());
    }
  }

  Future<void> logout() async {
    await _repo.logout();
    state = const AuthState();
  }
}

final authControllerProvider = StateNotifierProvider<AuthController, AuthState>((ref) {
  return AuthController(ref.read(authRepositoryProvider));
});
