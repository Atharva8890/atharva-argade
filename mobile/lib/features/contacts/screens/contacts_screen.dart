import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_colors.dart';

class ContactsScreen extends StatelessWidget {
  const ContactsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          const Padding(
            padding: EdgeInsets.fromLTRB(20, 16, 20, 8),
            child: Text('Contacts', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700)),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            child: TextField(
              decoration: const InputDecoration(
                hintText: 'Search contacts',
                prefixIcon: Icon(Icons.search),
              ),
            ),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 12),
              itemCount: _mockContacts.length,
              itemBuilder: (context, i) {
                final c = _mockContacts[i];
                return Card(
                  margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: AppColors.surfaceElev,
                      child: Text(c.name.substring(0, 1)),
                    ),
                    title: Text(c.name, style: const TextStyle(fontWeight: FontWeight.w600)),
                    subtitle: Text(c.language),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: <Widget>[
                        IconButton(icon: const Icon(Icons.chat_bubble_outline), onPressed: () {}),
                        IconButton(
                          icon: const Icon(Icons.phone, color: AppColors.electricBlue),
                          onPressed: () => context.push('/call/demo'),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

const List<({String name, String language})> _mockContacts = [
  (name: 'Priya Patil', language: 'मराठी (Marathi)'),
  (name: 'Raj Mehta', language: 'हिन्दी (Hindi)'),
  (name: 'Yuki Tanaka', language: '日本語 (Japanese)'),
  (name: 'Anna Müller', language: 'Deutsch (German)'),
  (name: 'Mateo García', language: 'Español (Spanish)'),
  (name: 'Liu Wei', language: '中文 (Chinese)'),
];
