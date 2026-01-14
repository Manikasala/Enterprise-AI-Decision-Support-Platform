"""Quick local tests for verifier/responders to ensure graceful fallback without Ollama."""
from retriever_agent import retrieve
from verifier_agent import verify
from responder_agent import respond

q = "What is the company's leave policy?"
ctx = retrieve(q)
print('retrieved (truncated):', ctx[:300])
verified = verify(ctx)
print('verified (truncated):', verified[:400])
final = respond(q, verified)
print('final (truncated):', final[:800])
