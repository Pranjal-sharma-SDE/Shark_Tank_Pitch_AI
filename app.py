import gradio as gr
import os
from dotenv import load_dotenv
from openai import OpenAI
from src.audio_analysis import VoiceAnalyzer
from src.content_analysis import ContentAnalyzer
from src.persona_engine import PersonaSynthesisEngine, SharkVoiceGenerator

# 1. Setup
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

FEEDBACK_DIR = "feedback_audio"
os.makedirs(FEEDBACK_DIR, exist_ok=True)

# 2. Main Processing Function
def process_pitch(audio_filepath):
    if not audio_filepath:
        return [None] * 11 # Return empty if no file

    # --- PIPELINE 1: AUDIO ANALYSIS ---
    voice_analyzer = VoiceAnalyzer(audio_filepath)
    acoustic_results = voice_analyzer.run_full_analysis()
    
    # Format Acoustic Output
    acoustic_txt = (
        f"**Emotion:** {acoustic_results['emotion']}\n"
        f"**Delivery Score:** {acoustic_results['delivery_score']}/100\n"
        f"**Hesitation:** {acoustic_results['metrics']['hesitation_index']}\n"
        f"**Pitch Var:** {acoustic_results['metrics']['pitch_variation']}"
    )

    # --- PIPELINE 2: CONTENT ANALYSIS ---
    content_analyzer = ContentAnalyzer(audio_filepath, client)
    business_results = content_analyzer.run_full_analysis()
    
    # Format Business Output
    scores = business_results['analysis'].get('scores', {})
    viability = business_results['analysis'].get('viability_score', 0)
    
    # --- PIPELINE 3: PERSONA & AUDIO GEN ---
    persona_engine = PersonaSynthesisEngine(acoustic_results, business_results, client)
    voice_gen = SharkVoiceGenerator(client)
    
    sharks = [
        ("The Royalty", "Mr. Wonderful"),
        ("The Tech Visionary", "Mark Cuban"),
        ("The Brand Guru", "Lori Greiner")
    ]
    
    outputs = [business_results['transcript'], acoustic_txt, scores, viability]
    
    # Generate Feedback + Audio for each Shark
    for persona_key, name in sharks:
        # Generate Text
        full_text = persona_engine.generate_feedback(persona_key)
        
        # Split Verdict
        if "FINAL RECOMMENDATION:" in full_text:
            parts = full_text.split("FINAL RECOMMENDATION:")
            monologue = parts[0].strip()
            verdict = parts[1].strip()
        else:
            monologue = full_text
            verdict = "Unknown"
            
        # Generate Audio
        audio_path = voice_gen.generate_audio(monologue, persona_key, FEEDBACK_DIR)
        
        # Add to outputs (Text, Verdict, Audio Path)
        outputs.extend([monologue, verdict, audio_path])
        
    return outputs

# 3. Gradio Interface
with gr.Blocks(title="Shark Tank AI") as app:
    gr.Markdown("# 🦈 Shark Tank Pitch Analyzer (Modular)")
    
    with gr.Row():
        with gr.Column(scale=1):
            audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Record Your Pitch")
            btn = gr.Button("Analyze Pitch", variant="primary")
        
        with gr.Column(scale=2):
            with gr.Tabs():
                with gr.TabItem("📊 Analysis"):
                    with gr.Row():
                        out_acoustic = gr.Markdown(label="Vocal Analysis")
                        out_viability = gr.Number(label="Viability Score")
                    out_scores = gr.JSON(label="Business Scores")
                    out_transcript = gr.Textbox(label="Transcript", lines=3)

    gr.Markdown("## 💬 The Sharks' Verdict")
    
    with gr.Row():
        # Shark 1
        with gr.Column():
            gr.Markdown("### Mr. Wonderful")
            out_k_text = gr.Textbox(label="Feedback", lines=4)
            out_k_verdict = gr.Label(label="Verdict")
            out_k_audio = gr.Audio(label="Listen", type="filepath")
            
        # Shark 2
        with gr.Column():
            gr.Markdown("### Mark Cuban")
            out_m_text = gr.Textbox(label="Feedback", lines=4)
            out_m_verdict = gr.Label(label="Verdict")
            out_m_audio = gr.Audio(label="Listen", type="filepath")

        # Shark 3
        with gr.Column():
            gr.Markdown("### Lori Greiner")
            out_l_text = gr.Textbox(label="Feedback", lines=4)
            out_l_verdict = gr.Label(label="Verdict")
            out_l_audio = gr.Audio(label="Listen", type="filepath")

    # Connect inputs/outputs
    # Outputs order: Transcript, Acoustic, Scores, Viability, 
    #                KevinTxt, KevinVer, KevinAud, 
    #                MarkTxt, MarkVer, MarkAud, 
    #                LoriTxt, LoriVer, LoriAud
    btn.click(
        fn=process_pitch,
        inputs=[audio_input],
        outputs=[
            out_transcript, out_acoustic, out_scores, out_viability,
            out_k_text, out_k_verdict, out_k_audio,
            out_m_text, out_m_verdict, out_m_audio,
            out_l_text, out_l_verdict, out_l_audio
        ]
    )

if __name__ == "__main__":
    app.launch()