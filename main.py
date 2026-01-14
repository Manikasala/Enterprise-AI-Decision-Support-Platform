from retriever_agent import retrieve
from verifier_agent import verify
from responder_agent import respond
from memory import store
from audit_logger import log

if __name__ == '__main__':
    import traceback
    # show quick system status to help debugging
    try:
        from responder_agent import llm_available
        from retriever_agent import _db
        llm_status = "available" if llm_available() else "unavailable"
    except Exception:
        llm_status = "unknown"
    print(f"System status: LLM={llm_status}, knowledge base directory='enterprise_db'")

    while True:
        q = input("\nAsk Enterprise Question: ")
        try:
            ctx = retrieve(q)
            verified = verify(ctx)
            final = respond(q, verified)

            store(q, str(final))
            log(q, str(final))
            print("\nAnswer:\n", final)
        except Exception as e:
            tb = traceback.format_exc()
            print("Error during processing. Full traceback written to 'error.log'.\n", e)
            with open('error.log', 'a', encoding='utf-8') as ef:
                ef.write('---\n')
                ef.write('query: ' + str(q) + '\n')
                ef.write(tb + '\n')
            # re-raise if you want the process to stop; we keep it running to allow next query
            # raise
