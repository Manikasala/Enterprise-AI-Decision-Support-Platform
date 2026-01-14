from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os, traceback, datetime

# lazy initialization so imports are fast and we can surface clear errors
_emb = None
_db = None

def _init():
    global _emb, _db
    if _emb is None:
        print("Initializing SentenceTransformer embeddings (may download model; this can take a few minutes)...")
        _emb = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    if _db is None:
        print("Connecting to Chroma DB at 'enterprise_db'...")
        _db = Chroma(persist_directory="enterprise_db", embedding_function=_emb)

# Fallback: extract raw text from the company PDF if embeddings/Chroma are unavailable
def _pdf_fallback():
    try:
        from pypdf import PdfReader
        candidates = ["data/company_docs.pdf", "company_docs.pdf/company_docs.pdf", "company_docs.pdf"]
        pdf_file = next((p for p in candidates if os.path.exists(p)), None)
        if pdf_file is None:
            return "[No knowledge base available (company_docs.pdf not found).]"
        reader = PdfReader(pdf_file)
        pages = []
        for p in reader.pages[:10]:  # read up to first 10 pages to be fast
            try:
                pages.append(p.extract_text() or "")
            except Exception:
                pages.append("")
        text = "\n\n".join(pages)
        return text or "[No text could be extracted from PDF]"
    except Exception as e:
        with open('error.log', 'a', encoding='utf-8') as ef:
            ef.write(f"[{datetime.datetime.now()}] PDF fallback failed: {e}\n")
            ef.write(traceback.format_exc() + '\n')
        return "[No knowledge base available (failed to read PDF).]"

def retrieve(task):
    # try to initialize embeddings/db but don't block the process for long - use PDF fallback if it takes too long
    try:
        from threading import Thread
        t = Thread(target=_init, daemon=True)
        t.start()
        t.join(5)  # wait up to 5 seconds for initialization
        if t.is_alive():
            print("Embedding initialization taking too long — using raw PDF fallback for a fast response.")
            return _pdf_fallback()
        # if init finished, but _db may still be None or fail on query
        if _db is None:
            print("Chroma DB not ready — using raw PDF fallback.")
            return _pdf_fallback()
        docs = _db.similarity_search(task, k=5)
        return "\n".join([d.page_content for d in docs])
    except Exception as e:
        # fallback to raw PDF extraction so the app can still return something useful
        print("Retriever unavailable; using raw PDF fallback. See error.log for details.")
        with open('error.log', 'a', encoding='utf-8') as ef:
            ef.write(f"[{datetime.datetime.now()}] Retriever error: {e}\n")
            ef.write(traceback.format_exc() + '\n')
        return _pdf_fallback()
