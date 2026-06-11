'use strict';

const db = require('../../config/db');
const config = require('../../config');
const { HttpError } = require('../../middleware/error');

const PLANS = {
  free: {
    code: 'free',
    name: 'Free',
    monthlyMinutes: 10,
    maxLanguages: 5,
    callRecording: false,
    transcriptExport: false,
    ads: true,
    priceInr: 0,
    priceUsd: 0,
  },
  premium: {
    code: 'premium',
    name: 'Premium',
    monthlyMinutes: -1,
    maxLanguages: -1,
    callRecording: true,
    transcriptExport: true,
    ads: false,
    priceInr: 299,
    priceUsd: 4.99,
  },
  business: {
    code: 'business',
    name: 'Business',
    monthlyMinutes: -1,
    maxLanguages: -1,
    callRecording: true,
    transcriptExport: true,
    ads: false,
    team: true,
    analytics: true,
    meetingTranslation: true,
    apiAccess: true,
    priceInr: 999,
    priceUsd: 14.99,
  },
};

const listPlans = () => Object.values(PLANS);

const ofUser = async (userId) => {
  const { rows } = await db.query(
    `SELECT subscription_plan, subscription_renews_at FROM users WHERE id = $1`,
    [userId]
  );
  if (!rows.length) throw new HttpError(404, 'User not found');
  const code = rows[0].subscription_plan || 'free';
  return { ...PLANS[code], renewsAt: rows[0].subscription_renews_at };
};

const createOrder = async (userId, { plan, gateway = 'razorpay' }) => {
  if (!PLANS[plan]) throw new HttpError(400, 'Unknown plan');
  const planDef = PLANS[plan];

  if (gateway === 'razorpay') {
    if (!config.payments.razorpay.keyId || !config.payments.razorpay.keySecret) {
      throw new HttpError(503, 'Razorpay not configured');
    }
    const Razorpay = require('razorpay');
    const rzp = new Razorpay({
      key_id: config.payments.razorpay.keyId,
      key_secret: config.payments.razorpay.keySecret,
    });
    const order = await rzp.orders.create({
      amount: planDef.priceInr * 100,
      currency: 'INR',
      notes: { userId, plan },
    });
    return { gateway: 'razorpay', order };
  }

  if (gateway === 'stripe') {
    if (!config.payments.stripe.secretKey) throw new HttpError(503, 'Stripe not configured');
    const stripe = require('stripe')(config.payments.stripe.secretKey);
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency: 'usd',
          recurring: { interval: 'month' },
          product_data: { name: `VoiceBridge AI - ${planDef.name}` },
          unit_amount: Math.round(planDef.priceUsd * 100),
        },
        quantity: 1,
      }],
      metadata: { userId, plan },
      success_url: 'voicebridge://billing/success?session_id={CHECKOUT_SESSION_ID}',
      cancel_url: 'voicebridge://billing/cancel',
    });
    return { gateway: 'stripe', session };
  }

  throw new HttpError(400, 'Unsupported gateway');
};

const setPlan = async (userId, plan, renewsAt) => {
  if (!PLANS[plan]) throw new HttpError(400, 'Unknown plan');
  await db.query(
    'UPDATE users SET subscription_plan = $1, subscription_renews_at = $2 WHERE id = $3',
    [plan, renewsAt || null, userId]
  );
  return { ok: true, plan };
};

module.exports = { listPlans, ofUser, createOrder, setPlan, PLANS };
