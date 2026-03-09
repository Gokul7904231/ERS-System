"""
Temporal Emotion Smoothing

Stabilizes webcam/video emotion predictions using a weighted frame buffer
and confidence threshold filtering.

Features:
  - Rolling buffer of the last N predictions
  - Recent frames weighted more heavily (recency bias)
  - Confidence-weighted majority voting
  - Low-confidence predictions filtered to "neutral"
  - Stability threshold: emotion must dominate ≥60% of buffer frames
"""

from collections import deque, Counter


# Confidence below this threshold → force "neutral"
CONFIDENCE_THRESHOLD = 0.45

# Emotion must appear in at least this fraction of frames to be accepted
STABILITY_THRESHOLD = 0.60


class TemporalEmotionSmoother:
    """Smooths emotion predictions over multiple frames."""

    def __init__(self, buffer_size=15):
        self.buffer_size = buffer_size
        self._buffer = deque(maxlen=buffer_size)  # (emotion, confidence) tuples
        self._last_stable_emotion = "neutral"
        self._last_stable_conf = 50.0

    def update(self, emotion, confidence):
        """
        Add a new prediction to the buffer and return the smoothed result.

        Args:
            emotion: predicted emotion string (e.g. "happy", "sad")
            confidence: float 0–100 (percentage)

        Returns:
            (smoothed_emotion, smoothed_confidence)
        """
        # --- Confidence filtering ---
        conf_frac = confidence / 100.0 if confidence > 1.0 else confidence
        if conf_frac < CONFIDENCE_THRESHOLD:
            emotion = "neutral"
            conf_frac = max(conf_frac, 0.45)

        self._buffer.append((emotion, conf_frac))

        return self._compute_smoothed()

    def _compute_smoothed(self):
        """Weighted majority vote with recency bias + stability threshold."""
        if not self._buffer:
            return ("neutral", 50.0)

        n = len(self._buffer)
        emotion_scores = {}
        emotion_confs = {}
        emotion_counts = Counter()

        for i, (emo, conf) in enumerate(self._buffer):
            # Recency weight: most recent frame gets weight = n, oldest gets weight = 1
            recency_weight = i + 1
            combined_weight = recency_weight * conf

            emotion_scores[emo] = emotion_scores.get(emo, 0.0) + combined_weight
            if emo not in emotion_confs:
                emotion_confs[emo] = []
            emotion_confs[emo].append(conf)
            emotion_counts[emo] += 1

        # Pick the emotion with the highest weighted score
        best_emotion = max(emotion_scores, key=emotion_scores.get)
        avg_conf = sum(emotion_confs[best_emotion]) / len(emotion_confs[best_emotion])

        # --- Stability threshold ---
        # Emotion must appear in ≥60% of buffer frames to be accepted
        dominance_ratio = emotion_counts[best_emotion] / n
        if dominance_ratio >= STABILITY_THRESHOLD or n < 5:
            # Accept the new emotion — it's dominant enough (or buffer is still filling)
            self._last_stable_emotion = best_emotion
            self._last_stable_conf = avg_conf * 100.0
        else:
            # Not dominant enough — keep the previous stable emotion
            best_emotion = self._last_stable_emotion
            avg_conf = self._last_stable_conf / 100.0

        # Convert back to percentage
        return (best_emotion, avg_conf * 100.0)

    def reset(self):
        """Clear the prediction buffer."""
        self._buffer.clear()
        self._last_stable_emotion = "neutral"
        self._last_stable_conf = 50.0

    @property
    def is_stable(self):
        """True if the buffer is full (predictions are maximally smoothed)."""
        return len(self._buffer) >= self.buffer_size

