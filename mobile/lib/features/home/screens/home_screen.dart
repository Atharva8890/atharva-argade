import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_colors.dart';
import '../../auth/state/auth_controller.dart';
import '../../contacts/screens/contacts_screen.dart';
import '../../settings/screens/settings_screen.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  int _index = 0;

  static const List<Widget> _pages = <Widget>[
    _CallsTab(),
    ContactsScreen(),
    SettingsScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_index],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _index,
        onTap: (i) => setState(() => _index = i),
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(icon: Icon(Icons.phone), label: 'Calls'),
          BottomNavigationBarItem(icon: Icon(Icons.people_outline), label: 'Contacts'),
          BottomNavigationBarItem(icon: Icon(Icons.settings_outlined), label: 'Settings'),
        ],
      ),
    );
  }
}

class _CallsTab extends ConsumerWidget {
  const _CallsTab();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(authControllerProvider).user;
    return SafeArea(
      child: ListView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        children: <Widget>[
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: <Widget>[
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text('Hello,', style: TextStyle(color: AppColors.textSecondary)),
                  Text(
                    user?['name'] ?? 'Friend',
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w700),
                  ),
                ],
              ),
              CircleAvatar(
                radius: 22,
                backgroundColor: AppColors.surface,
                child: const Icon(Icons.person, color: AppColors.textPrimary),
              ),
            ],
          ),
          const SizedBox(height: 20),
          _QuickCallCard(onTap: () => context.push('/contacts')),
          const SizedBox(height: 16),
          Row(
            children: <Widget>[
              const Text('Recent calls', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
              const Spacer(),
              TextButton(onPressed: () {}, child: const Text('See all')),
            ],
          ),
          ..._mockHistory.map((c) => _CallTile(call: c)),
        ],
      ),
    );
  }
}

class _QuickCallCard extends StatelessWidget {
  const _QuickCallCard({required this.onTap});

  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(20),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: AppColors.primaryGradient,
          borderRadius: BorderRadius.circular(20),
          boxShadow: const <BoxShadow>[
            BoxShadow(color: Color(0x55225BFF), blurRadius: 30, offset: Offset(0, 12)),
          ],
        ),
        child: Row(
          children: <Widget>[
            Container(
              width: 56,
              height: 56,
              decoration: BoxDecoration(
                color: Colors.white.withValues(alpha: 0.18),
                borderRadius: BorderRadius.circular(18),
              ),
              child: const Icon(Icons.translate, color: Colors.white, size: 28),
            ),
            const SizedBox(width: 14),
            const Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Text(
                    'Start a translated call',
                    style: TextStyle(fontSize: 17, fontWeight: FontWeight.w700, color: Colors.white),
                  ),
                  SizedBox(height: 4),
                  Text(
                    'Talk to anyone, in any language',
                    style: TextStyle(color: Colors.white70),
                  ),
                ],
              ),
            ),
            const Icon(Icons.arrow_forward_rounded, color: Colors.white),
          ],
        ),
      ),
    );
  }
}

class _CallTile extends StatelessWidget {
  const _CallTile({required this.call});

  final ({String name, String lang, String time, bool incoming, bool missed}) call;

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: AppColors.surfaceElev,
          child: Text(call.name.substring(0, 1), style: const TextStyle(fontWeight: FontWeight.w700)),
        ),
        title: Text(call.name, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Row(
          children: <Widget>[
            Icon(
              call.incoming ? Icons.call_received : Icons.call_made,
              size: 14,
              color: call.missed ? AppColors.danger : AppColors.success,
            ),
            const SizedBox(width: 6),
            Text('${call.lang} • ${call.time}', style: const TextStyle(color: AppColors.textSecondary)),
          ],
        ),
        trailing: IconButton(
          icon: const Icon(Icons.phone, color: AppColors.electricBlue),
          onPressed: () => GoRouter.of(context).push('/call/demo'),
        ),
      ),
    );
  }
}

const List<({String name, String lang, String time, bool incoming, bool missed})> _mockHistory = [
  (name: 'Priya Patil', lang: 'मराठी ↔ English', time: 'Today, 11:24', incoming: true, missed: false),
  (name: 'Raj Mehta', lang: 'हिन्दी ↔ English', time: 'Yesterday, 18:02', incoming: false, missed: false),
  (name: 'Yuki Tanaka', lang: '日本語 ↔ English', time: 'Mon, 09:48', incoming: true, missed: true),
  (name: 'Anna Müller', lang: 'Deutsch ↔ English', time: 'Sun, 14:15', incoming: false, missed: false),
];
