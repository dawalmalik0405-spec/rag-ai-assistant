from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
import torch
import chromadb
from text_extractor import extract_text_from_file


# ---------------- CHUNKING ----------------
def chunking(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)


# ---------------- EMBEDDINGS ----------------
device = "cuda" if torch.cuda.is_available() else "cpu"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": device}
)

def embed_chunks(chunks):
    return embeddings.embed_documents(chunks)


# ---------------- ID GENERATION ----------------
def generate_ids(chunks, filename, start_index=0):
    ids = []
    for i in range(len(chunks)):
        ids.append(f"{filename}_{start_index + i}")
    return ids


# ---------------- CHROMA SETUP ----------------
client = chromadb.PersistentClient(path="./chromadb_db")
collection = client.get_or_create_collection(name="documents", metadata={"hnsw:space": "cosine"})


# ---------------- STORE IN VECTOR DB ----------------
def store_vdb(chunks, vectors, filename):
    
    # get next ID number to avoid overwrite
    next_id = collection.count()
    
    ids = generate_ids(chunks, filename, next_id)

    # metadata (VERY IMPORTANT for real RAG)
    metadatas = [{"file": filename, "chunk_index": i} for i in range(len(chunks))]

    collection.add(
        documents=chunks,
        embeddings=vectors,
        ids=ids,
        metadatas=metadatas
    )

    return {
        "stored_chunks": len(chunks),
        "first_id": ids[0],
        "last_id": ids[-1]
    }


# ---------------- MAIN INGEST FUNCTION ----------------
def ingest_file(file_path, filename):
    text = extract_text_from_file(file_path)
    if not text or not text.strip():
        raise ValueError(f"No extractable text found in file: {filename}")

    chunks = chunking(text)
    if not chunks:
        raise ValueError(f"No chunks created for file: {filename}")

    vectors = embed_chunks(chunks)
    if not vectors:
        raise ValueError(f"Embedding failed for file: {filename}")

    
    result = store_vdb(chunks, vectors, filename)
    return result

# text  = extract_text_from_file("123.pdf")
# print(text)


