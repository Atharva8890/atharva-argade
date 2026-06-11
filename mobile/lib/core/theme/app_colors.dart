import 'package:flutter/material.dart';

class AppColors {
  AppColors._();

  static const Color black = Color(0xFF0A0A0B);
  static const Color surface = Color(0xFF121214);
  static const Color surfaceElev = Color(0xFF1A1A1D);
  static const Color border = Color(0xFF26262B);

  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFB0B0B8);
  static const Color textMuted = Color(0xFF6E6E76);

  static const Color electricBlue = Color(0xFF2B6BFF);
  static const Color electricBlueGlow = Color(0xFF4F8BFF);
  static const Color accentCyan = Color(0xFF00E0FF);
  static const Color success = Color(0xFF22C55E);
  static const Color danger = Color(0xFFEF4444);
  static const Color warning = Color(0xFFF59E0B);

  static const Gradient primaryGradient = LinearGradient(
    colors: <Color>[electricBlue, accentCyan],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );
}
