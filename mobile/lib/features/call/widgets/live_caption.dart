import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';

class CaptionEntry {
  CaptionEntry({
    required this.speaker,
    required this.original,
    required this.originalLang,
    required this.translated,
    required this.translatedLang,
    this.fromMe = false,
  });

  final String speaker;
  final String original;
  final String originalLang;
  final String translated;
  final String translatedLang;
  final bool fromMe;
}

class LiveCaption extends StatelessWidget {
  const LiveCaption({super.key, required this.entry, this.showTranslation = true});

  final CaptionEntry entry;
  final bool showTranslation;

  @override
  Widget build(BuildContext context) {
    final Color bubble = entry.fromMe ? AppColors.electricBlue.withValues(alpha: 0.12) : AppColors.surfaceElev;
    final Color accent = entry.fromMe ? AppColors.accentCyan : AppColors.electricBlueGlow;
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: bubble,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: accent.withValues(alpha: 0.25)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Row(
            children: <Widget>[
              CircleAvatar(
                radius: 12,
                backgroundColor: accent.withValues(alpha: 0.25),
                child: Text(entry.speaker.substring(0, 1), style: TextStyle(fontSize: 12, color: accent)),
              ),
              const SizedBox(width: 8),
              Text(entry.speaker, style: TextStyle(fontWeight: FontWeight.w600, color: accent)),
              const Spacer(),
              Text(entry.originalLang, style: const TextStyle(color: AppColors.textMuted, fontSize: 11)),
            ],
          ),
          const SizedBox(height: 8),
          Text(entry.original, style: const TextStyle(fontSize: 15)),
          if (showTranslation) ...[
            const SizedBox(height: 6),
            Row(
              children: <Widget>[
                const Icon(Icons.arrow_downward, size: 12, color: AppColors.textMuted),
                const SizedBox(width: 4),
                Text(entry.translatedLang, style: const TextStyle(color: AppColors.textMuted, fontSize: 11)),
              ],
            ),
            const SizedBox(height: 4),
            Text(
              entry.translated,
              style: const TextStyle(fontSize: 14, color: AppColors.textSecondary, fontStyle: FontStyle.italic),
            ),
          ],
        ],
      ),
    );
  }
}
