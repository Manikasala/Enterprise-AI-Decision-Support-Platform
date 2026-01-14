import time, traceback
print('test_run starting')
start = time.time()
try:
    from retriever_agent import retrieve
    print('imported retrieve')
    # run retrieve with a timeout so we don't hang indefinitely
    import threading
    result = {}
    def run():
        try:
            result['value'] = retrieve('test')
        except Exception as e:
            result['error'] = e
            import traceback as _tb
            result['tb'] = _tb.format_exc()

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(60)  # wait up to 60 seconds
    if t.is_alive():
        print('retrieve() is taking longer than 60s — it may be downloading a model or building the DB. Please wait or run `ingest.py` first.')
    else:
        if 'error' in result:
            print('retrieve error:', result['error'])
            print(result.get('tb',''))
        else:
            res = result.get('value')
            print('retrieve returned type:', type(res))
            if res is None:
                print('retrieve returned None')
            else:
                print('length:', len(res))
                print(res[:400])
except Exception as e:
    print('error during test_run:', e)
    print(traceback.format_exc())

print('elapsed:', time.time() - start)
print('\nDone')
