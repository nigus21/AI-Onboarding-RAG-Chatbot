

<img src="https://upload.wikimedia.org/wikipedia/commons/0/0e/Umbrella_Corporation_logo.svg" alt="Umbrella Corporation Logo" width="100"/>

### Umbrella Corp Onboarding RAG Assistant

This project is a **production-style onboarding assistant** for the fictional **Umbrella Corporation**.  
It combines a **Streamlit UI**, **LangChain**, and a **local Chroma vector store** to answer employee questions about company policies using **Retrieval Augmented Generation (RAG)**, enriched with **personalized employee data**.

This is not just a template exercise – the app is fully implemented, wired to real components, and ready to run.

---

### What the App Does

- **Personalized onboarding chat**
  - Loads synthetic employee data (name, role, department, skills, etc.) from `data/employees.py`.
  - Keeps employee context and full conversation history in Streamlit session state.

- **Policy‑aware answers via RAG**
  - Ingests `data/umbrella_corp_policies.pdf` into a **Chroma** vector store using **OpenAI embeddings**.
  - Retrieves the most relevant policy chunks for each user question and feeds them into a LangChain prompt.

- **Modern chat UI**
  - Built with Streamlit, using `st.chat_message` and `st.chat_input`.
  - Streams LLM responses token‑by‑token for a responsive feel.

- **Robust behavior**
  - Handles vector store failures (for example OpenAI quota errors) gracefully instead of crashing.
  - Clean separation between UI (`gui.py`), assistant logic (`assistant.py`), and configuration / prompts (`prompts.py`).

---

### Tech Stack

<p align="left">
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit" height="32"/>
  <img src="https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/static/img/favicon.ico" alt="LangChain" height="32" style="margin-left:12px;"/>
  <img src="https://avatars.githubusercontent.com/u/125533846?s=200&v=4" alt="ChromaDB" height="32" style="margin-left:12px;"/>
  <img src="https://raw.githubusercontent.com/openai/openai-python/main/app_icon.png" alt="OpenAI" height="32" style="margin-left:12px;"/>
  <img src="https://raw.githubusercontent.com/groq/groq-python/main/app_icon.png" alt="Groq" height="32" style="margin-left:12px;"/>
  <img src="https://www.python.org/static/community_logos/python-logo.png" alt="Python" height="32" style="margin-left:12px;"/>
</p>

- **Frontend / UX**: Streamlit
- **Orchestration**: LangChain (`langchain`, `langchain-core`, `langchain-community`)
- **LLM**: `ChatGroq` with `llama-3.1-8b-instant` (can be swapped for other models)
- **Embeddings + Vector Store**: `OpenAIEmbeddings` + `Chroma`
- **PDF ingestion**: `PyPDFLoader` + `RecursiveCharacterTextSplitter`
- **Env & config**: `python-dotenv`

---

### Architecture at a Glance

- **`app.py`**
  - Entry point (`streamlit run app.py`).
  - Loads environment variables, configures logging, and sets Streamlit page options.
  - Caches:
    - `get_user_data()` – synthetic employee record.
    - `init_vector_store()` – builds the Chroma vector store from the PDF.
  - Instantiates:
    - `Assistant` (LLM + retrieval + prompt wiring).
    - `AssistantGUI` (chat interface).

- **`assistant.py`**
  - `Assistant` class encapsulates the LangChain pipeline:
    - Builds a `ChatPromptTemplate` that includes:
      - system prompt (`SYSTEM_PROMPT`),
      - conversation history,
      - current user input,
      - retrieved policy context,
      - employee information.
    - Streams responses via `self.chain.stream(user_input)`.
    - Safely degrades when `vector_store` is `None` (e.g. embedding API quota exceeded).

- **`gui.py`**
  - `AssistantGUI.render()`:
    - Renders existing messages from `st.session_state.messages`.
    - Accepts a new question via `st.chat_input`.
    - Streams the assistant’s answer and appends it back into session state.

- **`prompts.py`**
  - Contains:
    - `SYSTEM_PROMPT`: carefully designed persona + behavior for the Umbrella onboarding assistant.
    - `WELCOME_MESSAGE`: first AI message shown in the chat.

- **`data/employees.py`**
  - Generates realistic synthetic employee data used to personalize answers.

---

### Getting Started

- **1. Clone and create a virtual environment**

```bash
git clone https://github.com/nigus21/AI-Onboarding-RAG-Chatbot.git
cd AI-Onboarding-RAG-Chatbot
python -m venv venv
venv\Scripts\activate  # on Windows
```

- **2. Install dependencies**

```bash
pip install -r requirements.txt
```

- **3. Configure API keys**

Create a `.env` file in the project root and set the keys you need, for example:

```text
OPENAI_API_KEY=your_openai_key_here
GROQ_API_KEY=your_groq_key_here
```

- **4. Run the app**

```bash
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`) in your browser.

---

### How to Use the App

- The app automatically:
  - Loads a synthetic Umbrella employee profile.
  - Builds (and caches) a vector store from the Umbrella policies PDF.
  - Greets the user with a themed welcome message.

- Then you can ask questions like:
  - “What are the safety protocols in the lab?”
  - “What is the leave policy for my position?”
  - “Which security clearances apply to my department?”

The model answers in‑character as an Umbrella onboarding assistant, grounded in:
- The specific employee's data.
- The policy chunks retrieved from the vector store.

---

### Notes for Reviewers / Hiring Managers

- The project demonstrates:
  - **End‑to‑end ownership**: from UX and caching to model orchestration and error handling.
  - **Practical RAG implementation**: PDF ingestion, chunking, embeddings, retrieval.
  - **Good engineering hygiene**: separation of concerns, environment management, and Git version control.
- The app is easily extensible:
  - Swap embeddings or vector store.
  - Plug in a different LLM.
  - Attach to a real employee database instead of synthetic data.

If you’d like, I can walk through the codebase and design decisions file by file. 