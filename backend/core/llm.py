from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from functools import lru_cache
import torch

MODEL_NAME = "google/flan-t5-base"  # Upgrade from 'small' to 'base' for better quality

@lru_cache(maxsize=1)
def load_model_and_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

def generate_answer(question: str, context: str) -> str:
    tokenizer, model = load_model_and_tokenizer()

    prompt = (
        f"Answer the question based on the following context:\n\n"
        f"{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer:"
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=768)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,   # Increased to allow longer answers
            temperature=0.3,
            top_p=0.9,
            do_sample=True,
            num_return_sequences=1
        )

    answer = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Remove redundant prefix
    if answer.lower().startswith("answer:"):
        answer = answer[len("answer:"):].strip()

    return answer
