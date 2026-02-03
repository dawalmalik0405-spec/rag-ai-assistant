
import os 


# def search_query(query, collection, embeddings, filename=None):
  
  # query = embeddings.embed_query(query)

  # if filename:
  #   filter = {"file": filename}
  #   results  = collection.query(
  #     query_embeddings=[query],
  #     where=filter,
  #     n_results=5,
  #     include=["documents", "metadatas","distances"] 
  #   )
  # else:
    
  #   results  = collection.query(
  #     query_embeddings=[query],
  #     n_results=5,
  #     include=["documents", "metadatas","distances"] 
  #   )

  # relevant_chunks = []
  # for i, doc in enumerate(results["documents"][0]):
  #     relevant_chunks.append({
  #         "content": doc,
  #         "metadata": results["metadatas"][0][i],
  #         "id": results["ids"][0][i],
  #         "similarity": 1 - results["distances"][0][i]  # Convert distance to similarity
  #     })
    
  # return relevant_chunks

def search_query(query, collection, embeddings, filename=None):


    if not filename:
        raise ValueError("Filename is required for retrieval")

    query_embedding = embeddings.embed_query(query)

    query_args = {
        "query_embeddings": [query_embedding],
        "where":{"file":filename},
        "n_results": 6,
        "include": ["documents", "metadatas", "distances"]
    }




    results = collection.query(**query_args)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    chunks = []
    for doc,meta,dist in zip(documents, metadatas, distances):
        chunks.append({
            "content": doc,
            "metadata": meta,
            "similarity": 1 - dist
        })

    return chunks

