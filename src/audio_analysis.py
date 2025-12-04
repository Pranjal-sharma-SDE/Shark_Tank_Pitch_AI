import librosa
import numpy as np
import scipy.signal

class VoiceAnalyzer:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        try:
            self.y, self.sr = librosa.load(audio_path, sr=None)
        except Exception as e:
            print(f"Error loading audio: {e}")
            self.y, self.sr = None, None

    def analyze_pitch(self):
        f0, voiced_flag, voiced_probs = librosa.pyin(
            self.y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7')
        )
        valid_pitch = f0[~np.isnan(f0)]
        
        if len(valid_pitch) == 0:
            return {"avg_pitch_hz": 0, "pitch_variation": 0, "f0_series": []}

        return {
            "avg_pitch_hz": round(np.mean(valid_pitch), 2),
            "pitch_variation": round(np.std(valid_pitch), 2),
            "f0_series": valid_pitch
        }

    def analyze_volume(self):
        rms = librosa.feature.rms(y=self.y)[0]
        return {
            "avg_volume": round(float(np.mean(rms)), 4),
            "volume_dynamic_range": round(float(np.max(rms) - np.min(rms)), 4),
            "rms_series": rms
        }

    def analyze_fluency(self, f0_series, rms_series):
        non_silent = librosa.effects.split(self.y, top_db=20)
        non_silent_dur = sum((end - start) / self.sr for start, end in non_silent)
        total_dur = librosa.get_duration(y=self.y, sr=self.sr)
        
        hesitation_index = (total_dur - non_silent_dur) / total_dur if total_dur > 0 else 0

        if len(f0_series) > 0:
            pitch_derivative = np.abs(np.diff(f0_series))
            flat_pitch_frames = np.sum(pitch_derivative < 2.0) 
            monotone_ratio = flat_pitch_frames / len(f0_series)
        else:
            monotone_ratio = 0

        return {
            "hesitation_index": round(hesitation_index, 2),
            "monotone_ratio": round(monotone_ratio, 2)
        }

    def detect_emotional_tone(self, pitch_data, vol_data, fluency_data):
        pitch_var = pitch_data.get("pitch_variation", 0)
        vol_range = vol_data.get("volume_dynamic_range", 0)
        pace = fluency_data.get("hesitation_index", 0)

        if pitch_var > 40 and vol_range > 0.05:
            return "Enthusiastic / Excited"
        elif pitch_var < 10 and vol_range < 0.02:
            return "Bored / Monotone"
        elif pace > 0.30:
            return "Nervous / Hesitant"
        else:
            return "Confident / Balanced"

    def calculate_delivery_score(self, pitch_data, vol_data, fluency_data):
        score = 100
        pv = pitch_data['pitch_variation']
        if pv < 15: score -= 20
        elif pv > 80: score -= 10
        
        hes = fluency_data['hesitation_index']
        if hes > 0.20: score -= (hes * 100)
        
        vol = vol_data['volume_dynamic_range']
        if vol < 0.02: score -= 15
        
        return max(0, int(score))

    def run_full_analysis(self):
        if self.y is None: return {}
        
        pitch = self.analyze_pitch()
        volume = self.analyze_volume()
        fluency = self.analyze_fluency(pitch['f0_series'], volume['rms_series'])
        emotion = self.detect_emotional_tone(pitch, volume, fluency)
        score = self.calculate_delivery_score(pitch, volume, fluency)
        
        return {
            "metrics": {**pitch, **volume, **fluency},
            "emotion": emotion,
            "delivery_score": score
        }