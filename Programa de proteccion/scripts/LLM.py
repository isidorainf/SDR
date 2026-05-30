from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from template import template_mitigacion
import torch
import gc

gc.collect()
torch.cuda.empty_cache() if torch.cuda.is_available() else None

model_path = "Qwen/Qwen2.5-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_path,
    tokenizer=model_path,
    device_map="auto",
    dtype=torch.float16,
    do_sample=True,
    temperature=0.01,
    top_p=0.9,
    max_new_tokens=256,
    return_full_text=False
)

llm = HuggingFacePipeline(pipeline=pipe)
cadena_mitigacion = template_mitigacion | llm
