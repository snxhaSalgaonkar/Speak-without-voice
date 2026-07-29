/**
 * Frontend Application Constants
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const HEALTH_ENDPOINT = `${API_BASE_URL}/api/v1/health`;
export const PREDICT_ENDPOINT = `${API_BASE_URL}/api/v1/predict`;

export const SUPPORTED_GESTURES = [
  'Hello',
  'Thanks',
  'Yes',
  'No',
  'I Love You',
];

export const CONFIDENCE_THRESHOLDS = {
  HIGH: 0.85,
  MEDIUM: 0.70,
};
