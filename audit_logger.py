import json, datetime

def log(q, answer):
    with open("audit_log.json","a") as f:
        json.dump({"time":str(datetime.datetime.now()),"query":q,"answer":answer},f)
        f.write("\n")
