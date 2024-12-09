from llama_index.core import VectorStoreIndex, StorageContext, Document
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.storage.docstore.simple_docstore import SimpleDocumentStore
from llama_index.core.vector_stores.simple import SimpleVectorStore, DEFAULT_VECTOR_STORE
from llama_index.core.graph_stores.simple import SimpleGraphStore
from llama_index.core.storage.index_store.simple_index_store import SimpleIndexStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.retrievers.bm25 import BM25Retriever
from llama_index.core.retrievers import QueryFusionRetriever
from sentence_transformers import SentenceTransformer
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings


def build_index(raginformation):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # 1. Combine Resume and JD for Each Profile
    documents = [
        Document(
            text=f"Resume: {profile['resume']} JobDescription: {profile['job_description']}",
            extra_info={
                "job_title": profile["job_title"],
                "resume": profile["resume"],
                "job_description": profile["job_description"]
            }
        )
        for profile in raginformation
    ]

    # 2. Initialize Required Stores
    docstore = SimpleDocumentStore()
    vector_store = SimpleVectorStore()
    graph_store = SimpleGraphStore()
    index_store = SimpleIndexStore()

    # 3. Initialize StorageContext
    storage_context = StorageContext(
        docstore=docstore,
        index_store=index_store,
        # vector_stores=vector_store,
        vector_stores={DEFAULT_VECTOR_STORE: vector_store},
        graph_store=graph_store
    )

    Settings.llm = OpenAI(temperature=0.1, model="gpt-4")
    # Settings.llm = OpenAI()
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.node_parser = SentenceSplitter(chunk_size=2048, chunk_overlap=20)
    Settings.context_window = 3900

    # 4. Create VectorStoreIndex
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context,
                                            transformations=[SentenceSplitter(chunk_size=2048)])

    return index


def combine_text_list(resume_data, jd_data):
    combined_text = (
        f"Education: {resume_data.get('Education', '')}\n"
        f"Skills: {resume_data.get('Skills', '')}\n"
        f"Experience: {resume_data.get('Experience', '')}\n"
        f"Projects: {resume_data.get('Projects', '')}\n\n"
        f"Role: {jd_data.get('Role', '')}\n"
        f"Qualification: {jd_data.get('Qualification', '')}\n"
        f"Title: {jd_data.get('Title', '')}\n"
    )
    return combined_text


def retrieve_top_profiles(index, combined_text, similarity_top_k=5, retriever_weights=[0.6, 0.4]):
    """
    Retrieves the top profiles based on the combined_text using a QueryFusionRetriever.

    Args:
        index: The VectorStoreIndex object.
        combined_text (str): The combined text containing resume and job description.
        similarity_top_k (int): Number of top results to retrieve. Default is 2.
        retriever_weights (list): Weights for combining vector and BM25 retrievers. Default is [0.6, 0.4].

    Returns:
        list: A list of top profiles with job title, resume, and job description.
    """
    # Initialize BM25 and Vector Retrievers
    bm25_retriever = BM25Retriever.from_defaults(
        docstore=index.docstore, similarity_top_k=similarity_top_k
    )
    vector_retriever = index.as_retriever(similarity_top_k=similarity_top_k + 3)

    # Combine retrievers using QueryFusionRetriever
    retriever = QueryFusionRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        retriever_weights=retriever_weights,
        similarity_top_k=similarity_top_k,
        num_queries=1,  # Disable query generation
        mode="dist_based_score",  # Use distance-based score mode
        use_async=False,  # Synchronous mode
        verbose=True,
    )

    # Retrieve nodes with scores
    nodes_with_scores = retriever.retrieve(combined_text)

    # Process the retrieved results
    top_profiles = []
    for node in nodes_with_scores:
        extra_info = node.node.extra_info  # Metadata from the document
        top_profiles.append({
            "job_title": extra_info["job_title"],
            "resume": extra_info["resume"],
            "job_description": extra_info["job_description"],
        })

    return top_profiles
