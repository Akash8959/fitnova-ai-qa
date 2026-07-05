# FitNova AI QA Pipeline

An end-to-end AI-powered Quality Assurance (QA) pipeline for analyzing fitness sales calls.

This project was built as part of an AI Engineer take-home assignment for FitNova, a Bangalore-based phone-sales fitness coaching company. The objective was to ingest recorded calls, transcribe conversations, separate speakers, evaluate call quality using a Large Language Model (LLM), detect coaching issues, store the complete analysis in PostgreSQL, and expose the results through a FastAPI API.

The assignment's primary success criterion was:

> **At least one call must successfully complete the entire pipeline — from ingestion to database persistence — and be retrievable through an API.**

This requirement has been fully implemented and verified using a real PostgreSQL database, a local Faster-Whisper transcription model, a local Ollama-hosted LLM, and FastAPI.

---

## Features

- Folder-based audio ingestion with duplicate detection (idempotent via unique `source_id`)
- Local speech-to-text transcription using Faster-Whisper
- Speaker diarisation (Tier 1 heuristic implementation)
- LLM-based call quality scoring against a fixed rubric
- Structured issue-flag detection from a fixed taxonomy
- Transcript-backed hallucination guardrail (RapidFuzz quote verification)
- Deterministic weighted scoring, calculated in Python rather than trusted from the LLM
- PostgreSQL persistence using SQLAlchemy and Alembic migrations
- FastAPI endpoint for retrieving complete per-call analysis
- Provider abstraction allowing the LLM backend to be swapped (e.g. to Anthropic) without changing pipeline logic

---

## Architecture

The implemented Tier 1 pipeline processes each call through five stages:

1. Audio Ingestion
2. Transcription & Speaker Labelling
3. LLM Quality Analysis
4. Database Persistence
5. API Surfacing
   A sixth stage — **Human Feedback & Continuous Improvement** (e.g. advisors disputing flags, team leaders reviewing disputes) — is part of the intended system design but is **not implemented** in this Tier 1 submission. It is listed under Future Improvements below.

```text
sample_call.mp3
        │
        ▼
Folder Adapter (Ingestion)
        │
        ▼
PostgreSQL (calls row created, idempotent on source_id)
        │
        ▼
Faster-Whisper (Transcription)
        │
        ▼
Transcript + Transcript Segments (speaker, start_time, end_time, text)
        │
        ▼
Heuristic Diarisation (alternating Speaker A / Speaker B)
        │
        ▼
Ollama LLM Analysis (rubric scores + issue flags, structured JSON)
        │
        ▼
Hallucination Guardrail (RapidFuzz quote verification against transcript)
        │
        ▼
Deterministic Weighted Score (calculated in Python)
        │
        ▼
Scores + Flags stored in PostgreSQL
        │
        ▼
FastAPI GET /results/{call_id}
```

---

## Real vs Simplified Components

| Component                         | Implementation                                                                  | Status          |
| --------------------------------- | ------------------------------------------------------------------------------- | --------------- |
| PostgreSQL database               | Real                                                                            | ✅              |
| SQLAlchemy ORM                    | Real                                                                            | ✅              |
| Alembic migrations                | Real                                                                            | ✅              |
| Folder ingestion                  | Real                                                                            | ✅              |
| Duplicate detection / idempotency | Real                                                                            | ✅              |
| Faster-Whisper transcription      | Real                                                                            | ✅              |
| Transcript + segment persistence  | Real                                                                            | ✅              |
| LLM scoring pipeline              | Real                                                                            | ✅              |
| Deterministic score calculation   | Real                                                                            | ✅              |
| Hallucination guardrail           | Real                                                                            | ✅              |
| Provider abstraction (analysis)   | Real                                                                            | ✅              |
| FastAPI API                       | Real                                                                            | ✅              |
| Speaker diarisation               | Tier 1 heuristic (alternating speakers)                                         | ⚠️ Simplified |
| Anthropic integration             | Replaced with local Ollama provider (`llama3.2:3b`) behind the same interface | ⚠️ Simplified |

Scope items not covered by this table (organizational assignment, sample audio domain, single-call processing) are documented under **Known Limitations** below, since they are scope decisions rather than technical substitutions.

---

## Project Structure

```
fitnova-ai-qa/
│
├── app/
│   ├── api/                  # FastAPI routes (results endpoint)
│   ├── core/                 # Configuration
│   ├── db/                   # Database session/engine setup
│   ├── models/                # SQLAlchemy models
│   ├── repositories/         # Data access layer
│   ├── schemas/
│   ├── services/
│   │   ├── ingestion/         # FolderAdapter, IngestionService
│   │   ├── transcription/     # WhisperProvider, TranscriptionService
│   │   ├── diarization/       # HeuristicProvider, DiarizationService
│   │   └── analysis/          # OllamaProvider, AnalyzerService, Guardrail
│   ├── utils/
│   └── main.py                # FastAPI app entrypoint
│
├── alembic/                   # Database migrations
├── scripts/                   # Pipeline entrypoint scripts
├── sample_calls/               # Sample audio + metadata
├── tests/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Tech Stack

| Category       | Technology               |
| -------------- | ------------------------ |
| Language       | Python 3.11              |
| API            | FastAPI                  |
| Database       | PostgreSQL               |
| ORM            | SQLAlchemy               |
| Migrations     | Alembic                  |
| Speech-to-Text | Faster-Whisper           |
| LLM            | Ollama (`llama3.2:3b`) |
| Validation     | Pydantic                 |
| Fuzzy Matching | RapidFuzz                |
| Server         | Uvicorn                  |

---

## Prerequisites

| Software   | Version (Recommended) |
| ---------- | --------------------- |
| Python     | 3.11+                 |
| PostgreSQL | 16+                   |
| Git        | Latest                |
| Ollama     | Latest                |

Docker Desktop is **not required** for this project. The application was developed and verified using a local Python environment with PostgreSQL and Ollama running natively.

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fitnova-ai-qa
```

### 2. Create a Virtual Environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Environment Variables

Copy the example environment file:

**Windows**

```powershell
copy .env.example .env
```

**Linux / macOS**

```bash
cp .env.example .env
```

Update the values inside `.env` to match your local environment:

```env
DATABASE_URL=postgresql://postgres:<your-password>@localhost:5432/fitnova_ai
 
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
 
WHISPER_MODEL=tiny
APP_ENV=development
```

`.env` is excluded from version control via `.gitignore`. Never commit a real `.env` file.

---

## Database Setup

### 1. Create the PostgreSQL Database

```bash
psql -U postgres
```

```sql
CREATE DATABASE fitnova_ai;
\q
```

### 2. Apply Database Migrations

```bash
alembic upgrade head
```

This creates all required tables:

- `organizations`
- `teams`
- `advisors`
- `calls`
- `transcripts`
- `transcript_segments`
- `scores`
- `flags`
  **No seed script is required.** `advisor_id` on `calls` is nullable — verified at the code level (ingestion never sets it), the SQLAlchemy model level (`nullable=True`), and the live PostgreSQL schema level (`is_nullable = YES`). Calls can be ingested, transcribed, diarised, and analyzed without first creating an organization, team, or advisor. This is a deliberate Tier 1 scope decision, not an architectural claim about how the system should work long-term — see Known Limitations.

---

## Ollama Setup

### 1. Install Ollama

Install from [https://ollama.com](https://ollama.com), then verify:

```bash
ollama --version
```

### 2. Download the Required Model

```bash
ollama pull llama3.2:3b
```

This downloads the model only — it does **not** confirm the Ollama service is running.

### 3. Start (or Confirm) the Ollama Service

On Windows, start the Ollama desktop application if it isn't already running. Verify the service is responding:

```bash
ollama list
```

If installed models are listed successfully, the service is running and ready to accept requests.

---

## Running the End-to-End Pipeline

The following commands execute the verified Tier 1 pipeline, in order.

### 1. Ingest the Sample Call

```bash
python -m scripts.ingest_call
```

This reads audio from `sample_calls/` and creates a new `Call` record in PostgreSQL (idempotent — re-running on the same file does not create a duplicate).

### 2. Transcribe the Audio

```bash
python -m scripts.transcribe_call
```

### 3. Perform Speaker Diarisation

```bash
python -m scripts.diarize_call
```

### 4. Run LLM Analysis

```bash
python -m scripts.analyze_call
```

This stage evaluates the transcript, generates rubric scores, detects issue flags, validates structured JSON output, verifies quoted transcript lines using the hallucination guardrail, computes the deterministic weighted score, and stores the results in PostgreSQL.

> **Tier 1 processing model**
>
> The current implementation processes **one call at a time**. The processing scripts (`transcribe_call.py`, `diarize_call.py`, and `analyze_call.py`) select the **first `Call` row** in the database (`db.query(Call).first()`) rather than accepting a `call_id` as input.
>
> For a clean end-to-end run, ensure the database contains only the call you intend to process (or that it is the oldest unprocessed call). Selecting arbitrary calls by ID in the processing scripts is a planned future enhancement — the API layer, unlike the scripts, already supports querying by a specific `call_id`.

### 5. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

### 6. Retrieve the Results

Open the interactive API documentation:

```
http://127.0.0.1:8000/docs
```

Or request the endpoint directly:

```
GET /results/{call_id}
```

A successful response includes call metadata, the full transcript with speaker labels and timestamps, all five rubric scores plus the deterministic overall score, and all guardrail-verified issue flags with severity, quoted line, and reason.

---

## API Documentation

### `GET /results/{call_id}`

Returns the complete analysis for a single call.

**Example response:**

```json
{
  "call_id": 2,
  "file_name": "sample_call.mp3",
  "language": "en",
  "duration_seconds": 126.01,
  "score": {
    "needs_discovery": 4,
    "product_knowledge": 5,
    "objection_handling": 3,
    "compliance": 5,
    "next_step_booking": 5,
    "overall_score": 87.0
  },
  "flags": [
    {
      "issue_type": "weak_or_missing_trial_booking",
      "severity": "medium",
      "timestamp_in_call": "00:01:26",
      "quoted_line": "You're very welcome. Goodbye.",
      "reason": "Customer was not offered a trial period before the call ended."
    }
  ],
  "transcript": [
    {
      "speaker": "Speaker A",
      "start_time": 0.0,
      "end_time": 2.0,
      "text": "Call is now being recorded."
    }
  ]
}
```

If `call_id` does not exist, the endpoint returns `404 Call not found`.

---

## Design Decisions

**Provider abstraction for LLM analysis.** The original assignment referenced Anthropic. Because no Anthropic API key was available, Tier 1 uses a local Ollama-hosted `llama3.2:3b` model behind a provider interface (`AnalyzerProvider`). The interface means Anthropic — or any other hosted LLM — can be introduced later by implementing a new provider class, without changing the rest of the pipeline.

**Deterministic weighted score.** This was not a simplification — it is a reliability improvement. The LLM evaluates each rubric dimension, but the application computes the final weighted score itself in Python, eliminating arithmetic inconsistencies from the local model (observed directly during testing: the LLM's own reported weighted score did not match the correct calculation from its own rubric values).

**Hallucination guardrail.** This is a real production-style safeguard, not a mock. Every flag's quoted line is verified against the actual stored transcript using fuzzy matching (RapidFuzz) before being persisted. Flags with no sufficiently similar match in the transcript are discarded or downgraded rather than stored as confirmed findings.

**Nullable `advisor_id`.** Tier 1 focuses on proving the AI QA pipeline end to end. Associating calls with organizations, teams, and advisors is a separate workflow that was intentionally deferred to a future iteration, so calls can currently be processed without an advisor. The schema already supports the relationship (`advisor_id` is a nullable foreign key to `advisors`), so this functionality can be added later without a schema redesign.

**Idempotent ingestion.** Each ingested call is keyed by a unique `source_id`. Re-running ingestion against the same file does not create a duplicate `Call` row — verified directly (first run creates a call, second run detects and skips the duplicate).

---

## Known Limitations

**1. Speaker Diarisation.** Tier 1 uses a deterministic heuristic that alternates speaker labels between Speaker A and Speaker B. This demonstrates the end-to-end pipeline but will mislabel consecutive turns from the same speaker (observed directly in testing, where one speaker asking several questions in a row was split across both labels). A production system would replace this with a dedicated diarisation model such as `pyannote.audio`.

**2. Local LLM instead of Anthropic.** The assignment referenced Anthropic for analysis. Tier 1 uses a local Ollama-hosted `llama3.2:3b` model behind a provider abstraction due to the absence of an API key. Smaller local models are also less reliable at producing fully self-consistent structured output than a hosted model like Claude — for example, an issue tag and its accompanying reason have occasionally been observed to be semantically inconsistent (e.g. a flag for `no_needs_discovery` paired with a reason describing appropriate discovery behavior). The hallucination guardrail catches unsupported quotes, but it does not verify semantic correctness of the model's reasoning.

**3. Advisor Assignment Workflow.** The current pipeline allows calls to be processed without an assigned advisor. This is a deliberate Tier 1 scope decision to prioritize proving the end-to-end pipeline before building organizational assignment workflows. As a direct consequence, this Tier 1 build has no mechanism for a Team Leader or Sales Director to view calls grouped by team or advisor — that view depends on organizational assignment, which is intended for a future iteration.

**4. Sample Audio.** The included sample recording is a generic customer-service conversation (a retail exchange call) rather than a FitNova-specific fitness sales call. The pipeline itself is domain-agnostic, but the rubric scores and detected issues are less representative than they would be against a real fitness-coaching sales conversation.

**5. Single-Call Processing Workflow.** The current orchestration scripts (`transcribe_call.py`, `diarize_call.py`, `analyze_call.py`) process the first `Call` row in the database and do not accept a `call_id` parameter. This is sufficient for the verified Tier 1 demonstration but is not intended for concurrent or batch processing. A future version would support explicit call selection and queue-based orchestration.

---

## Future Improvements

- Replace heuristic diarisation with `pyannote.audio` for genuine speaker separation
- Swap the Ollama provider for a hosted LLM (e.g. Anthropic) via the existing provider interface
- Build organization/team/advisor assignment workflows and role-based dashboards (Sales Director, Team Leader, Advisor views)
- Add a dispute/review flow for advisors to contest flags, with a review log
- Support explicit `call_id` selection and queue-based/batch processing in the orchestration scripts
- Source-agnostic ingestion adapters for telephony and CRM vendors, beyond the current folder-drop adapter
- PII redaction pass on stored transcripts
- Non-sales-call classification to route wrong-number/internal calls out of scoring
- Retry/backoff wrapping for all external API calls

---

## Submission Notes

This repository represents a working Tier 1 implementation: one real call is ingested, transcribed, diarised, analyzed, guardrail-verified, persisted to PostgreSQL, and surfaced via a FastAPI endpoint — verified end to end from a clean database state. Items listed under Known Limitations and Future Improvements were consciously scoped out to prioritize a complete, verified pipeline over broader but partially-implemented feature coverage.
