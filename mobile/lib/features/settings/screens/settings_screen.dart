import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_colors.dart';
import '../../auth/state/auth_controller.dart';

class SettingsScreen extends ConsumerWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authControllerProvider).user;
    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        children: <Widget>[
          const Text('Settings', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700)),
          const SizedBox(height: 20),
          Card(
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Row(
                children: <Widget>[
                  const CircleAvatar(
                    radius: 28,
                    backgroundColor: AppColors.surfaceElev,
                    child: Icon(Icons.person, color: AppColors.textPrimary, size: 28),
                  ),
                  const SizedBox(width: 14),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: <Widget>[
                        Text(user?['name'] ?? 'Guest', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                        Text(user?['email'] ?? '', style: const TextStyle(color: AppColors.textSecondary)),
                        const SizedBox(height: 4),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                          decoration: BoxDecoration(
                            color: AppColors.electricBlue.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: Text(
                            (user?['subscription_plan'] ?? 'free').toString().toUpperCase(),
                            style: const TextStyle(
                              fontSize: 10,
                              fontWeight: FontWeight.w700,
                              color: AppColors.accentCyan,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  IconButton(icon: const Icon(Icons.edit_outlined), onPressed: () {}),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          _Section(title: 'Preferences', tiles: <Widget>[
            _SettingsTile(
              icon: Icons.language,
              title: 'Preferred language',
              subtitle: user?['language'] ?? 'en',
              onTap: () {},
            ),
            _SettingsTile(icon: Icons.dark_mode_outlined, title: 'Theme', subtitle: 'Dark', onTap: () {}),
            _SettingsTile(icon: Icons.notifications_outlined, title: 'Notifications', onTap: () {}),
          ]),
          _Section(title: 'Voice & Translation', tiles: <Widget>[
            _SettingsTile(icon: Icons.record_voice_over_outlined, title: 'Voice cloning', subtitle: 'Premium', onTap: () {}),
            _SettingsTile(icon: Icons.noise_aware_outlined, title: 'AI noise cancellation', onTap: () {}),
            _SettingsTile(icon: Icons.translate, title: 'Default translation engine', onTap: () {}),
          ]),
          _Section(title: 'Account', tiles: <Widget>[
            _SettingsTile(
              icon: Icons.workspace_premium,
              title: 'Subscription',
              subtitle: 'View plans & upgrade',
              onTap: () => context.push('/subscription'),
            ),
            _SettingsTile(icon: Icons.shield_outlined, title: 'Privacy & security', onTap: () {}),
            _SettingsTile(icon: Icons.info_outline, title: 'About', onTap: () {}),
            _SettingsTile(
              icon: Icons.logout,
              title: 'Sign out',
              danger: true,
              onTap: () async {
                await ref.read(authControllerProvider.notifier).logout();
                if (context.mounted) context.go('/login');
              },
            ),
          ]),
        ],
      ),
    );
  }
}

class _Section extends StatelessWidget {
  const _Section({required this.title, required this.tiles});

  final String title;
  final List<Widget> tiles;

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        Padding(
          padding: const EdgeInsets.fromLTRB(4, 16, 4, 8),
          child: Text(
            title.toUpperCase(),
            style: const TextStyle(
              color: AppColors.textMuted,
              fontSize: 11,
              fontWeight: FontWeight.w700,
              letterSpacing: 1.2,
            ),
          ),
        ),
        Card(
          child: Column(children: tiles),
        ),
      ],
    );
  }
}

class _SettingsTile extends StatelessWidget {
  const _SettingsTile({
    required this.icon,
    required this.title,
    this.subtitle,
    required this.onTap,
    this.danger = false,
  });

  final IconData icon;
  final String title;
  final String? subtitle;
  final VoidCallback onTap;
  final bool danger;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon, color: danger ? AppColors.danger : AppColors.textPrimary),
      title: Text(
        title,
        style: TextStyle(
          color: danger ? AppColors.danger : AppColors.textPrimary,
          fontWeight: FontWeight.w600,
        ),
      ),
      subtitle: subtitle != null ? Text(subtitle!) : null,
      trailing: const Icon(Icons.chevron_right, color: AppColors.textMuted),
      onTap: onTap,
    );
  }
}
