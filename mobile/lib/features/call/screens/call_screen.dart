import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/theme/app_colors.dart';
import '../widgets/live_caption.dart';

class CallScreen extends ConsumerStatefulWidget {
  const CallScreen({super.key, required this.callId});

  final String callId;

  @override
  ConsumerState<CallScreen> createState() => _CallScreenState();
}

class _CallScreenState extends ConsumerState<CallScreen> {
  bool _muted = false;
  bool _speaker = true;
  bool _translate = true;
  bool _recording = false;
  Duration _elapsed = Duration.zero;
  Timer? _timer;

  final List<CaptionEntry> _captions = <CaptionEntry>[
    CaptionEntry(
      speaker: 'Priya',
      original: 'तुम्ही कसे आहात?',
      originalLang: 'मराठी',
      translated: 'How are you?',
      translatedLang: 'English',
    ),
    CaptionEntry(
      speaker: 'You',
      original: 'I am doing great, how was your day?',
      originalLang: 'English',
      translated: 'मी छान आहे, तुमचा दिवस कसा होता?',
      translatedLang: 'मराठी',
      fromMe: true,
    ),
  ];

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(const Duration(seconds: 1), (_) {
      setState(() => _elapsed += const Duration(seconds: 1));
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  String get _elapsedText {
    final m = _elapsed.inMinutes.toString().padLeft(2, '0');
    final s = (_elapsed.inSeconds % 60).toString().padLeft(2, '0');
    return '$m:$s';
  }

  Future<void> _endCall() async {
    _timer?.cancel();
    if (mounted) context.go('/home');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.black,
      body: SafeArea(
        child: Column(
          children: <Widget>[
            const SizedBox(height: 8),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Row(
                children: <Widget>[
                  IconButton(icon: const Icon(Icons.expand_more), onPressed: () => context.pop()),
                  const Spacer(),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                    decoration: BoxDecoration(
                      color: AppColors.success.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: <Widget>[
                        const _Pulse(color: AppColors.success),
                        const SizedBox(width: 6),
                        Text(
                          'Connected • $_elapsedText',
                          style: const TextStyle(color: AppColors.success, fontWeight: FontWeight.w600),
                        ),
                      ],
                    ),
                  ),
                  const Spacer(),
                  IconButton(
                    icon: const Icon(Icons.text_snippet_outlined),
                    onPressed: () => context.push('/transcript/${widget.callId}'),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 18),
            Container(
              width: 130,
              height: 130,
              decoration: const BoxDecoration(
                gradient: AppColors.primaryGradient,
                shape: BoxShape.circle,
              ),
              child: const Center(
                child: Text('P', style: TextStyle(fontSize: 56, fontWeight: FontWeight.w700, color: Colors.white)),
              ),
            ).animate(onPlay: (c) => c.repeat(reverse: true)).scale(
                  duration: 1400.ms,
                  begin: const Offset(1, 1),
                  end: const Offset(1.04, 1.04),
                  curve: Curves.easeInOut,
                ),
            const SizedBox(height: 16),
            const Text('Priya Patil', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700)),
            const SizedBox(height: 4),
            const Text(
              'मराठी ↔ English • AI translating',
              style: TextStyle(color: AppColors.textSecondary),
            ),
            const SizedBox(height: 18),
            Expanded(
              child: Container(
                margin: const EdgeInsets.symmetric(horizontal: 16),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: AppColors.surface,
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(color: AppColors.border),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Row(
                      children: <Widget>[
                        const Icon(Icons.closed_caption, color: AppColors.accentCyan, size: 18),
                        const SizedBox(width: 8),
                        const Text('Live captions', style: TextStyle(fontWeight: FontWeight.w600)),
                        const Spacer(),
                        Switch(
                          value: _translate,
                          onChanged: (v) => setState(() => _translate = v),
                          activeColor: AppColors.electricBlue,
                        ),
                      ],
                    ),
                    const Divider(),
                    Expanded(
                      child: ListView.separated(
                        itemCount: _captions.length,
                        separatorBuilder: (_, __) => const SizedBox(height: 12),
                        itemBuilder: (context, i) => LiveCaption(entry: _captions[i], showTranslation: _translate),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 18),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                _ControlButton(
                  icon: _muted ? Icons.mic_off : Icons.mic,
                  active: !_muted,
                  label: 'Mute',
                  onTap: () => setState(() => _muted = !_muted),
                ),
                _ControlButton(
                  icon: _speaker ? Icons.volume_up : Icons.hearing,
                  active: _speaker,
                  label: 'Speaker',
                  onTap: () => setState(() => _speaker = !_speaker),
                ),
                _ControlButton(
                  icon: _recording ? Icons.fiber_manual_record : Icons.fiber_manual_record_outlined,
                  active: _recording,
                  activeColor: AppColors.danger,
                  label: _recording ? 'Recording' : 'Record',
                  onTap: () => setState(() => _recording = !_recording),
                ),
                _ControlButton(
                  icon: Icons.translate,
                  active: _translate,
                  label: 'Translate',
                  onTap: () => setState(() => _translate = !_translate),
                ),
              ],
            ),
            const SizedBox(height: 18),
            GestureDetector(
              onTap: _endCall,
              child: Container(
                width: 76,
                height: 76,
                decoration: const BoxDecoration(color: AppColors.danger, shape: BoxShape.circle),
                child: const Icon(Icons.call_end, color: Colors.white, size: 34),
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }
}

class _ControlButton extends StatelessWidget {
  const _ControlButton({
    required this.icon,
    required this.active,
    required this.label,
    required this.onTap,
    this.activeColor = AppColors.electricBlue,
  });

  final IconData icon;
  final bool active;
  final String label;
  final VoidCallback onTap;
  final Color activeColor;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        GestureDetector(
          onTap: onTap,
          child: Container(
            width: 60,
            height: 60,
            decoration: BoxDecoration(
              color: active ? activeColor.withValues(alpha: 0.2) : AppColors.surface,
              shape: BoxShape.circle,
              border: Border.all(color: active ? activeColor : AppColors.border, width: 1.4),
            ),
            child: Icon(icon, color: active ? activeColor : AppColors.textSecondary),
          ),
        ),
        const SizedBox(height: 6),
        Text(label, style: const TextStyle(color: AppColors.textSecondary, fontSize: 12)),
      ],
    );
  }
}

class _Pulse extends StatelessWidget {
  const _Pulse({required this.color});

  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 8,
      height: 8,
      decoration: BoxDecoration(color: color, shape: BoxShape.circle),
    ).animate(onPlay: (c) => c.repeat()).fadeOut(duration: 800.ms);
  }
}
