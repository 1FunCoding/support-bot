I drafted this README based on your **BOverwhelm Support Bot** presentation. 

---

# Overwhelm Support Bot

A web-based support bot that helps **college students** manage **academic stress, burnout, and overwhelming workloads** by providing **tailored, empathetic guidance** based on a student’s **major** and **academic year**.

## Why this project

College students often face intense academic pressure and career-related worries. This bot aims to reduce barriers to support by offering **easy, anonymous access** to practical self-care tips, time-management strategies, and conversation-based follow-ups.

## Key features

* **Step-by-step questionnaire**: select major + academic year, optionally add specific concerns
* **Dynamic follow-up suggestions**: follow-up topics adapt to the chosen major
* **Chat interface**: ask additional questions in a conversational format
* **Start-over flow**: quickly restart a new session to explore different concerns

## How it works (high level)

1. **Frontend** collects the user’s major/year/concerns.
2. A **Flask backend** builds a customized prompt (major/year-aware) and sends it to the model.
3. The model returns **markdown-formatted** personalized guidance.
4. The app **converts markdown → HTML** and renders it in the browser.

## Model

* **Generative model (API call):** `gemini-3.0-flash`
* Chosen for strong natural-language performance and fast, context-specific responses across varied majors and school years.

## Tech stack

* **Backend:** Flask (Python)
* **Frontend:** Web UI (HTML/CSS/JS)
* **AI:** Gemini model via API
* **Rendering:** Markdown → HTML conversion for display

---

## Getting started

### Prerequisites

* Python 3.x
* A valid API key for the configured generative model provider

### Installation

```bash
git clone <your-repo-url>
cd <your-repo-folder>
python -m venv .venv
source .venv/bin/activate   # (macOS/Linux)
# .venv\Scripts\activate    # (Windows)

pip install -r requirements.txt
```

### Environment variables

Create a `.env` file (or export env vars) with your API credentials:

```bash
GEMINI_API_KEY="your_api_key_here"
```

### Run the app

```bash
flask run
```

Then open:

* `http://127.0.0.1:5000`

---

## Usage

1. Select your **major**
2. Select your **academic year**
3. (Optional) Add specific concerns (e.g., workload, interviews, group projects)
4. Get tailored support + suggested follow-up topics
5. Continue the conversation via chat, or click **Start Over**

---

## Safety & disclaimer

This project provides **general well-being support and study/workload guidance**. It is **not** a substitute for professional mental health care. If you’re in crisis or feel unsafe, contact local emergency services or your campus/local support resources.

---

## Future improvements

* Expand content coverage for more majors
* Add optional self-assessment surveys
* Provide curated links to professional/campus resources
* Improve prompt templates and evaluation of response quality

---

## Acknowledgements

* Built as a demo of how AI can provide accessible well-being support that **complements on-campus mental health services**.

---

If you paste your repo’s actual file structure (or your `app.py` / `requirements.txt`), I can tailor the **Setup**, **Project Structure**, and **Env Vars** sections to match your code exactly.
