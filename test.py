from vectordb import collection, embeddings
from retriver import search_query

results = search_query(
    "What is this mini project about?",
    collection,
    embeddings,
    # filename="Daval's Resume-hackerresume.pdf"
)

for r in results:
    print("FILE:", r["metadata"]["file"])
    print("TEXT:", r["content"][:150])
    print("-----")
