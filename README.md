# 🦈 Shark Tank Pitch Analyzer

**Master your pitch before you enter the Tank.**

The **Shark Tank Pitch Analyzer** is a multimodal AI application designed to help entrepreneurs evaluate the quality of their pitch. Unlike standard tools that only analyze text, this system listens to **how** you speak (vocal tone, hesitation, energy) and analyzes **what** you say (business logic, valuation, market fit).

It synthesizes this data to generate immersive, audio-visual feedback from AI agents modeled after famous investors: **"Mr. Wonderful"** (Kevin O'Leary), **"The Tech Visionary"** (Mark Cuban), and **"The Brand Guru"** (Lori Greiner).

-----

## 🚀 Key Features

### 1\. 🎤 Pipeline 1: Vocal Delivery Analysis (Acoustic Engine)

  * **Tone Detection:** Detects if you are Monotone, Enthusiastic, or Nervous.
  * **Fluency Metrics:** Calculates Hesitation Index (silence ratio) and Speaking Pace (syllables/sec).
  * **Delivery Score:** A quantitative score (0-100) based on confidence and clarity metrics using `Librosa`.

### 2\. 🧠 Pipeline 2: Business Logic Evaluation (Semantic Engine)

  * **Structure Recognition:** Automatically identifies your Hook, Problem, Solution, and Ask.
  * **VC Scoring:** Rates your pitch on 5 pillars: Problem Clarity, Solution Viability, Market Size, Business Model, and Valuation.
  * **Red Flag Detection:** Highlights logical fallacies or missing business data.

### 3\. 💬 Pipeline 3: Persona Synthesis & TTS (The "Sharks")

  * **AI Personas:** Generates distinct feedback in the style of specific investors (e.g., Kevin focuses on royalty deals; Mark focuses on tech).
  * **Audio Roast:** Uses OpenAI's Text-to-Speech (TTS) to generate `.wav` audio files of the feedback, so you can *hear* the Sharks critique you.
  * **Final Verdict:** Each Shark gives a definitive "Invest", "Not Invest", or "Need More Info" decision.

-----

## 📂 Project Structure

The project follows a modular architecture for maintainability:

```text
shark_tank_project/
├── .env                   # Environment variables (API Keys)
├── requirements.txt       # Python dependencies
├── app.py                 # Main Gradio Application (Entry Point)
├── feedback_audio/        # Directory for saving generated Shark audio files
└── src/                   # Source Code Modules
    ├── __init__.py
    ├── audio_analysis.py  # Pipeline 1: Signal processing (Librosa)
    ├── content_analysis.py# Pipeline 2: Transcription & Logic (Whisper/GPT-4o)
    └── persona_engine.py  # Pipeline 3: Feedback generation & TTS
```

-----

## 🛠️ Installation & Setup

### Prerequisites

  * Python 3.8 or higher
  * An [OpenAI API Key](https://platform.openai.com/) (Must support GPT-4o and Whisper)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/shark-tank-analyzer.git
cd shark_tank_project
```

### Step 2: Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

*Note: You may also need to install FFMPEG on your system for `librosa` and `gradio` audio processing to work correctly.*

### Step 4: Configure Environment Variables

Create a file named `.env` in the root directory and add your OpenAI API key:

```ini
OPENAI_API_KEY=sk-your-actual-api-key-here
```

-----

## ▶️ Usage

1.  **Run the Application:**

    ```bash
    python app.py
    ```

2.  **Access the Interface:**
    Open your web browser and navigate to the local URL provided in the terminal (usually `http://127.0.0.1:7860`).

3.  **Analyze Your Pitch:**

      * Click the microphone icon to **Record** your pitch directly (or upload a `.wav` file).
      * Click **"Analyze Pitch"**.
      * Wait for the pipelines to process (approx. 10-20 seconds).
      * View your **Scores**, read the **Transcripts**, and listen to the **Audio Feedback** from the Sharks.

-----

## 📊 Dashboard Preview

The interface provides:

  * **Visual Scorecards:** Real-time metrics on your vocal performance.
  * **Audio Players:** Individual playback controls for each Shark's feedback.
  * **Verdict Labels:** Quick status indicators (Invest/No Invest).

-----

## 🧩 Technologies Used

  * **[Gradio](https://gradio.app/):** Web interface and audio handling.
  * **[Librosa](https://librosa.org/):** Digital signal processing for pitch and rhythm analysis.
  * **[OpenAI API](https://openai.com/):**
      * **Whisper:** Speech-to-text transcription.
      * **GPT-4o:** Business logic analysis and persona simulation.
      * **TTS-1:** High-fidelity text-to-speech voice generation.
  * **NumPy / SciPy:** Mathematical operations for signal processing.

-----

## 🤝 Contributing

Contributions are welcome\! Please follow these steps:

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

-----


