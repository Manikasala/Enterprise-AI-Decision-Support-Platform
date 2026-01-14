from langchain_community.chat_models import ChatOllama
import traceback, datetime

_llm = None

def _init_llm():
    global _llm
    if _llm is None:
        try:
            _llm = ChatOllama(model="mistral")
        except Exception as e:
            # log and keep _llm as None to trigger fallback behavior
            with open('error.log', 'a', encoding='utf-8') as ef:
                ef.write(f"[{datetime.datetime.now()}] Failed to initialize Ollama model 'mistral': {e}\n")
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
            ef.write(f"[{datetime.datetime.now()}] Ollama call failed: {e}\n")
            ef.write(traceback.format_exc() + '\n')
        return None

# A safe fallback that returns context-based content if the LLM isn't available.
def _fallback_answer(q, verified):
    header = "[LLM unavailable — returning supporting content instead]\n"
    body = "" if not verified else verified
    footer = "\n\nTip: install/pull the 'mistral' model for Ollama and run the Ollama daemon, or configure OpenAI credentials to use OpenAI as an alternative.\n"
    return header + (body[:4000] if body else "No supporting content available.") + footer

def llm_available():
    _init_llm()
    return _llm is not None


def respond(q, verified):
    prompt = f"Answer:\n{q}\nUsing:\n{verified}"
    res = _call_llm(prompt)
    if res is None:
        return _fallback_answer(q, verified)
    return res
