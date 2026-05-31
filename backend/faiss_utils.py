import faiss
import numpy as np


def create_faiss_index(embeddings):

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(
        np.array(embeddings).astype("float32")
    )

    return index
def search_chunks(
    query_embedding,
    index,
    k=2
):

    distances, indices = index.search(
        np.array([query_embedding]).astype("float32"),
        k
    )

    return indices[0]
