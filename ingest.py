from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings

import os

# look for the company PDF in a few sensible locations
pdf_paths = ["data/company_docs.pdf", "company_docs.pdf/company_docs.pdf", "company_docs.pdf"]
pdf_file = next((p for p in pdf_paths if os.path.exists(p)), None)
if pdf_file is None:
    raise FileNotFoundError(
        "company_docs.pdf not found. Place it in 'data/company_docs.pdf' or 'company_docs.pdf/company_docs.pdf'."
    )

loader = PyPDFLoader(pdf_file)
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="enterprise_db"
)
db.persist()

print("Enterprise knowledge base ready. PDF used:", pdf_file)
