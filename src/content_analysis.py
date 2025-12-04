import json
import os

class ContentAnalyzer:
    def __init__(self, audio_path, client):
        self.audio_path = audio_path
        self.client = client
        self.transcript = ""

    def transcribe_audio(self):
        try:
            with open(self.audio_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            self.transcript = transcription.text
            return self.transcript
        except Exception as e:
            print(f"Transcription Error: {e}")
            return None

    def analyze_business_logic(self):
        if not self.transcript:
            return {"error": "No transcript available"}

        system_prompt = """
        You are a VC Analyst. Analyze the pitch transcript for BUSINESS LOGIC.
        
        TASK 1: Extract Structure (Hook, Problem, Solution, Ask).
        TASK 2: Score 1-10 (Problem, Solution, Market, Model, Ask).
        TASK 3: Calculate Overall Viability Score (0-100).
        
        Output JSON format:
        {
            "pitch_structure": {"hook_segment": "...", "problem_segment": "...", "solution_segment": "...", "ask_segment": "..."},
            "scores": {"problem": 0, "solution": 0, "market": 0, "model": 0, "ask": 0},
            "viability_score": 0,
            "missing_elements": [],
            "red_flags": [],
            "summary_critique": "..."
        }
        """

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self.transcript}
            ],
            response_format={"type": "json_object"} 
        )
        return json.loads(response.choices[0].message.content)

    def run_full_analysis(self):
        self.transcribe_audio()
        analysis = self.analyze_business_logic()
        return {"transcript": self.transcript, "analysis": analysis}