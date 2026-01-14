from langchain_community.chat_models import ChatOllama
import traceback, datetime

_llm = None

def _init_llm():
    global _llm
    if _llm is None:
        try:
            _llm = ChatOllama(model="mistral")
        except Exception as e:
            with open('error.log', 'a', encoding='utf-8') as ef:
                ef.write(f"[{datetime.datetime.now()}] Failed to initialize Ollama model 'mistral' for verifier: {e}\n")
                ef.write(traceback.format_exc() + '\n')
            _llm = None

def _call_llm(prompt):
    _init_llm()
    if _llm is None:
        return None
    try:
        return _llm.invoke(prompt)
    except Exception as e:
        with open('error.log', 'a', encoding='utf-8') as ef:
            ef.write(f"[{datetime.datetime.now()}] Ollama call failed in verifier: {e}\n")
            ef.write(traceback.format_exc() + '\n')
        return None

# Fallback verifier returns the raw context or a short check message
def llm_available():
    _init_llm()
    return _llm is not None


def _fallback_verify(context):
    if not context:
        return "[LLM unavailable — no context provided to verify]"
    snippet = context[:4000]
    return f"[LLM unavailable — returning context for local verification]\n{snippet}"

def verify(context):
    prompt = f"Verify facts:\n{context}"
    res = _call_llm(prompt)
    if res is None:
        return _fallback_verify(context)
    return res
