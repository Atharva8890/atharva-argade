import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:socket_io_client/socket_io_client.dart' as io;

import '../constants.dart';
import '../storage/secure_storage.dart';

final socketClientProvider = Provider<SocketClient>((ref) {
  final storage = ref.read(secureStorageProvider);
  return SocketClient(storage);
});

class SocketClient {
  SocketClient(this._storage);

  final AppSecureStorage _storage;
  io.Socket? _socket;

  Future<io.Socket> connect() async {
    if (_socket != null && _socket!.connected) return _socket!;
    final token = await _storage.readAccessToken();
    _socket = io.io(
      AppConstants.socketUrl,
      io.OptionBuilder()
          .setTransports(<String>['websocket'])
          .disableAutoConnect()
          .setAuth(<String, dynamic>{'token': token})
          .build(),
    );
    _socket!.connect();
    return _socket!;
  }

  io.Socket? get socket => _socket;

  void disconnect() {
    _socket?.disconnect();
    _socket = null;
  }
}
