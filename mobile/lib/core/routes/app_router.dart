import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../features/auth/screens/forgot_password_screen.dart';
import '../../features/auth/screens/login_screen.dart';
import '../../features/auth/screens/otp_screen.dart';
import '../../features/auth/screens/signup_screen.dart';
import '../../features/call/screens/call_screen.dart';
import '../../features/contacts/screens/contacts_screen.dart';
import '../../features/home/screens/home_screen.dart';
import '../../features/meetings/screens/meeting_screen.dart';
import '../../features/settings/screens/settings_screen.dart';
import '../../features/splash/screens/splash_screen.dart';
import '../../features/subscription/screens/subscription_screen.dart';
import '../../features/transcript/screens/transcript_screen.dart';

final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    initialLocation: '/',
    routes: <RouteBase>[
      GoRoute(path: '/', builder: (context, state) => const SplashScreen()),
      GoRoute(path: '/login', builder: (context, state) => const LoginScreen()),
      GoRoute(path: '/signup', builder: (context, state) => const SignupScreen()),
      GoRoute(
        path: '/otp',
        builder: (context, state) => OtpScreen(target: (state.extra as String?) ?? ''),
      ),
      GoRoute(path: '/forgot-password', builder: (context, state) => const ForgotPasswordScreen()),
      GoRoute(path: '/home', builder: (context, state) => const HomeScreen()),
      GoRoute(path: '/contacts', builder: (context, state) => const ContactsScreen()),
      GoRoute(
        path: '/call/:callId',
        builder: (context, state) => CallScreen(callId: state.pathParameters['callId']!),
      ),
      GoRoute(
        path: '/transcript/:callId',
        builder: (context, state) => TranscriptScreen(callId: state.pathParameters['callId']!),
      ),
      GoRoute(path: '/subscription', builder: (context, state) => const SubscriptionScreen()),
      GoRoute(path: '/settings', builder: (context, state) => const SettingsScreen()),
      GoRoute(path: '/meetings', builder: (context, state) => const MeetingScreen()),
    ],
  );
});
