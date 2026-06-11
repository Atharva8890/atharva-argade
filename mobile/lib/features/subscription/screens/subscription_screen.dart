import 'package:flutter/material.dart';

import '../../../core/theme/app_colors.dart';

class SubscriptionScreen extends StatelessWidget {
  const SubscriptionScreen({super.key});

  static const List<({String code, String name, String price, List<String> features, bool highlight})> _plans = [
    (code: 'free', name: 'Free', price: '₹0 / month', features: <String>[
      '10 minutes daily',
      '5 languages',
      'Ads enabled',
    ], highlight: false),
    (code: 'premium', name: 'Premium', price: '₹299 / month', features: <String>[
      'Unlimited calls',
      '100+ languages',
      'Call recording',
      'Transcript export',
      'No ads',
    ], highlight: true),
    (code: 'business', name: 'Business', price: '₹999 / month', features: <String>[
      'Team accounts',
      'Analytics dashboard',
      'Meeting translation',
      'API access',
      'Priority support',
    ], highlight: false),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Choose your plan')),
      body: ListView(
        padding: const EdgeInsets.all(20),
        children: <Widget>[
          const Text(
            'Talk in any language without limits.',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
          ),
          const SizedBox(height: 6),
          const Text(
            'Upgrade to unlock real-time AI translation for unlimited calls.',
            style: TextStyle(color: AppColors.textSecondary),
          ),
          const SizedBox(height: 20),
          ..._plans.map((p) => _PlanCard(plan: p)),
        ],
      ),
    );
  }
}

class _PlanCard extends StatelessWidget {
  const _PlanCard({required this.plan});

  final ({String code, String name, String price, List<String> features, bool highlight}) plan;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.surface,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: plan.highlight ? AppColors.electricBlue : AppColors.border,
          width: plan.highlight ? 1.6 : 1,
        ),
        gradient: plan.highlight
            ? LinearGradient(
                colors: <Color>[
                  AppColors.electricBlue.withValues(alpha: 0.10),
                  AppColors.surface,
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              )
            : null,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Row(
            children: <Widget>[
              Text(
                plan.name,
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w700),
              ),
              const SizedBox(width: 8),
              if (plan.highlight)
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                  decoration: BoxDecoration(
                    color: AppColors.electricBlue,
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: const Text(
                    'POPULAR',
                    style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.w700),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 4),
          Text(plan.price, style: const TextStyle(color: AppColors.accentCyan, fontSize: 16)),
          const SizedBox(height: 14),
          ...plan.features.map(
            (f) => Padding(
              padding: const EdgeInsets.symmetric(vertical: 3),
              child: Row(
                children: <Widget>[
                  const Icon(Icons.check_circle, color: AppColors.success, size: 18),
                  const SizedBox(width: 8),
                  Expanded(child: Text(f)),
                ],
              ),
            ),
          ),
          const SizedBox(height: 14),
          SizedBox(
            width: double.infinity,
            height: 46,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: plan.highlight ? AppColors.electricBlue : AppColors.surfaceElev,
              ),
              onPressed: () {},
              child: Text(plan.code == 'free' ? 'Current plan' : 'Upgrade to ${plan.name}'),
            ),
          ),
        ],
      ),
    );
  }
}
