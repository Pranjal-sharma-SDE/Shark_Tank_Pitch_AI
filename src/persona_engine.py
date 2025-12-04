import os
import uuid
import datetime

class PersonaSynthesisEngine:
    def __init__(self, acoustic_full_results, business_full_results, client):
        self.acoustic_data = acoustic_full_results
        self.business_data = business_full_results.get('analysis', {})
        self.transcript = business_full_results.get('transcript', "")
        self.client = client
        self.interpreted_acoustics = self._interpret_acoustic_data()

    def _interpret_acoustic_data(self):
        metrics = self.acoustic_data.get('metrics', {})
        emotion = self.acoustic_data.get('emotion', "Unknown")
        score = self.acoustic_data.get('delivery_score', 0)
        
        summary = f"Tone: {emotion}. Score: {score}/100."
        if metrics.get('hesitation_index', 0) > 0.20: summary += " High hesitation."
        if metrics.get('pitch_variation', 0) < 15: summary += " Monotone."
        return summary

    def generate_feedback(self, persona_type):
        system_prompt = f"""
        You are {persona_type} on Shark Tank.
        Critique the pitch based on the data.
        End your response with this exact line:
        "FINAL RECOMMENDATION: [Invest / Not Invest / Need More Info]"
        """
        
        user_context = f"""
        Data:
        - Vocal: {self.interpreted_acoustics}
        - Viability: {self.business_data.get('viability_score')}/100
        - Ask Score: {self.business_data.get('scores', {}).get('ask')}/10
        - Transcript: "{self.transcript[:300]}..."
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_context}
            ],
            temperature=0.8
        )
        return response.choices[0].message.content

class SharkVoiceGenerator:
    def __init__(self, client):
        self.client = client

    def generate_audio(self, text, persona_type, output_folder):
        voice_map = {
            "The Royalty": "onyx",       
            "The Tech Visionary": "echo", 
            "The Brand Guru": "nova"     
        }
        
        # Clean text (remove the label for the audio read)
        clean_text = text.split("FINAL RECOMMENDATION:")[0]
        
        # Generate Unique Filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:4]
        filename = f"{persona_type.replace(' ', '_')}_{timestamp}_{unique_id}.wav"
        full_path = os.path.join(output_folder, filename)

        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice_map.get(persona_type, "alloy"),
                input=clean_text,
                response_format="wav"
            )
            response.stream_to_file(full_path)
            return full_path
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None