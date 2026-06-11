import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../../../core/theme/app_colors.dart';

class TranscriptScreen extends StatelessWidget {
  const TranscriptScreen({super.key, required this.callId});

  final String callId;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Transcript'),
        actions: <Widget>[
          IconButton(
            icon: const Icon(Icons.copy_all),
            onPressed: () {
              final text = _mockTranscript.map((e) => '${e.speaker}: ${e.original}\n→ ${e.translated}').join('\n\n');
              Clipboard.setData(ClipboardData(text: text));
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Transcript copied to clipboard')),
              );
            },
          ),
          IconButton(icon: const Icon(Icons.download), onPressed: () {}),
          IconButton(icon: const Icon(Icons.share), onPressed: () {}),
        ],
      ),
      body: ListView.separated(
        padding: const EdgeInsets.all(16),
        itemCount: _mockTranscript.length,
        separatorBuilder: (_, __) => const SizedBox(height: 12),
        itemBuilder: (context, i) {
          final e = _mockTranscript[i];
          return Card(
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Row(
                    children: <Widget>[
                      Text(e.speaker, style: const TextStyle(fontWeight: FontWeight.w600)),
                      const Spacer(),
                      Text(e.time, style: const TextStyle(color: AppColors.textMuted, fontSize: 12)),
                    ],
                  ),
                  const SizedBox(height: 6),
                  Text(e.original),
                  const SizedBox(height: 4),
                  Text(
                    '→ ${e.translated}',
                    style: const TextStyle(color: AppColors.textSecondary, fontStyle: FontStyle.italic),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}

const List<({String speaker, String original, String translated, String time})> _mockTranscript = [
  (speaker: 'Priya', original: 'तुम्ही कसे आहात?', translated: 'How are you?', time: '00:02'),
  (speaker: 'You', original: 'I am doing great, how was your day?', translated: 'मी छान आहे, तुमचा दिवस कसा होता?', time: '00:08'),
  (speaker: 'Priya', original: 'खूप छान! आज मी ऑफिसमध्ये नवीन प्रोजेक्ट सुरू केला.', translated: 'Wonderful! I started a new project at the office today.', time: '00:18'),
  (speaker: 'You', original: 'That sounds exciting. Tell me more!', translated: 'हे खूप रोमांचक वाटतं. आणखी सांगा!', time: '00:25'),
];
