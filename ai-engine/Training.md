# Training the MindBridge AI Engine

## What's running right now (Stage 0)

`ai-engine/responder.py` is not a trained model — it's pattern matching
(`GREETING_PATTERNS`) plus keyword lookup (`KNOWLEDGE_BASE`). That's why it
can already do this, today, with zero training and zero external API calls:

```
User: hi
Engine: Hi Steve! I'm here and ready to listen. How are you doing today, and how can I help?
```

This matters more than it sounds like: it's honest (it only responds
confidently where it actually has a matching rule, and falls back
otherwise), it's fully auditable (every response traces to a line of code
you wrote), and it costs nothing to run. Keep this as your **safety
backstop** even after you add a real model — the crisis-keyword screening
in `mentalhealth/services.py` already works the same way, and that layer
should never depend on a model's judgment alone.

The path from here to "a real trained model" has three stages. You don't
need to build all three before this is useful — Stage 0 alone already
handles greetings and simple lookups correctly.

---

## Stage 1: Retrieval (RAG) — teaches it facts, no training required

Instead of a hardcoded `KNOWLEDGE_BASE` list, you embed a real corpus
(doctor-reviewed guidance, FAQ content, therapeutic frameworks) and search
it by meaning instead of exact keywords.

```
pip install sentence-transformers chromadb

# 1. Build the corpus once (or whenever content is updated)
from sentence_transformers import SentenceTransformer
import chromadb

embedder = SentenceTransformer("BAAI/bge-small-en-v1.5")  # runs locally, no API
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection("mental_health_kb")

docs = [
    {"id": "anxiety-1", "text": "When anxiety shows up before a big event, grounding techniques like..."},
    # ... your doctor-reviewed content, one chunk per entry
]
collection.add(
    ids=[d["id"] for d in docs],
    embeddings=embedder.encode([d["text"] for d in docs]).tolist(),
    documents=[d["text"] for d in docs],
)

# 2. At request time, in responder.py:
def retrieve(prompt: str, k: int = 3) -> list[str]:
    query_vec = embedder.encode([prompt]).tolist()
    results = collection.query(query_embeddings=query_vec, n_results=k)
    return results["documents"][0]
```

You then feed the retrieved chunks into either (a) more rule-based
templating, or (b) a small local LLM as context — which is Stage 2.

This is the single highest-leverage thing to build next: it's how the
engine goes from "3 hardcoded topics" to "hundreds of topics," without
any GPU or training run.

---

## Stage 2: A real local model, fine-tuned on your data

This is what "train it like OpenAI" actually means in practice — not
training from scratch (that costs the kind of money only OpenAI/Anthropic-
scale labs spend), but taking an existing open-weight model and adapting
it to your domain.

**1. Pick a small base model you can run locally:**
- `Qwen2.5-1.5B-Instruct` or `Phi-3-mini` — run fine on a decent CPU or a
  single consumer GPU
- `Llama-3.1-8B-Instruct` — needs a real GPU (rent one hourly on
  RunPod/Lambda/Vast.ai if you don't own one)

**2. Build your training dataset** — this is the part that actually needs
your time. Format: instruction/response pairs, ideally written or reviewed
by a clinician for this domain:

```jsonl
{"prompt": "hi", "response": "Hi! I'm here and ready to listen. How are you doing today?"}
{"prompt": "I've been feeling really anxious about work", "response": "That sounds stressful..."}
```

Start with 200-500 solid examples. Quality matters far more than volume at
this stage — a small, clean, clinician-reviewed dataset beats a huge scraped
one.

**3. Fine-tune with LoRA** (parameter-efficient — trains a small adapter,
not the whole model, so it's cheap and fast):

```python
# train.py — minimal LoRA fine-tune sketch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
from datasets import load_dataset

base_model = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(base_model)

lora_config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05, task_type="CAUSAL_LM")
model = get_peft_model(model, lora_config)

dataset = load_dataset("json", data_files="training_data.jsonl")["train"]

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=TrainingArguments(
        output_dir="./mindbridge-lora",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        learning_rate=2e-4,
    ),
)
trainer.train()
model.save_pretrained("./mindbridge-lora")
```

**4. Serve it** — swap `responder.py`'s `generate_response()` to load this
model instead of (or in addition to — keep the rule-based greeting/crisis
paths regardless) the pattern matcher. For real throughput, serve via
`vLLM` or `Ollama` rather than raw `transformers` in production.

---

## "Trains itself over time" — what that should actually mean

Be deliberate here, because this is the part that goes wrong in most
DIY projects. There are two very different things people mean by this:

**❌ Live weight updates from every conversation, in real time.**
Don't do this. It's how a model silently absorbs bad advice, manipulation
attempts, or unsafe content from a single conversation and starts repeating
it to the next person. There's no review step, no way to catch it, and no
way to roll it back cleanly. This is a real failure mode other chatbots
have hit publicly — worth avoiding deliberately, not just by default.

**✅ A scheduled retrain loop with a human in it.** This is what you
actually want, and it's exactly what the `CrisisEscalation` model and
`Message.risk_flag` fields I built into `mentalhealth/models.py` are for:

```
1. Real conversations happen → logged (already done, in your DB)
2. Periodically (weekly/monthly), export anonymized conversations
3. A clinician/reviewer reads them, corrects bad responses, approves good ones
4. Reviewed examples get added to training_data.jsonl
5. Re-run the Stage 2 fine-tune → new LoRA adapter version
6. Evaluate the new version against a held-out test set BEFORE deploying
7. Deploy the new adapter; keep the previous one so you can roll back
```

This gets you genuine improvement over time without the safety problems of
live updates. It's slower, but it's the version of "self-training" that
doesn't put users at risk in the meantime.

---

## Where to start, concretely

Given where you are right now (Stage 0 running, auth working):

1. Ship Stage 0 as-is for greetings/simple cases — it already works.
2. Build the Stage 1 RAG corpus next — even 20-30 doctor-reviewed entries
   beats the current 3-topic hardcoded list, and needs no training.
3. Only move to Stage 2 fine-tuning once you have real (or clinician-
   authored) conversation examples to train on — a model fine-tuned on 50
   made-up examples isn't better than what you have now.