# MindBridge AI Engine

The local inference service Django calls via `AI_ENGINE_URL`. Runs entirely
on your machine — no OpenAI/Anthropic/other third-party API calls.

## Run it

```bash
cd ai-engine
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 9000 --reload
```

Then in your Django `.env`, make sure:
```
AI_ENGINE_URL=http://localhost:9000
```

Test it directly:
```bash
curl -X POST http://localhost:9000/v1/infer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hi", "user_display_name": "Steve", "profile": "full"}'
```

Expected response:
```json
{"text": "Hi Steve! I'm here and ready to listen. How are you doing today, and how can I help?", "model_version": "stage0_rules_v1"}
```

## What's here today vs. what's next

- `responder.py` — the actual response logic. Currently rule-based
  (pattern matching + a small keyword-matched knowledge base).
- `main.py` — the FastAPI wrapper Django talks to.

See `TRAINING_GUIDE.md` for how this evolves into retrieval (RAG) and then
a real fine-tuned local model, and how to make it improve over time safely.