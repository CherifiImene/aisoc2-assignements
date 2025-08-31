from helpers import ChromaUtils

collection_name = ""
chromadb_collection = ChromaUtils().init_chroma(collection_name, task="create")


def upsert_message_pair(chat_uid: str, user_query: str, assistant_response: str, metadata: list = None):
    """
    Stores (user_query, assistant_response) as a document in Chroma
    """
    
    if metadata is None:
        metadata = []
    
    # store the chat uid + the response in the metadata
    # while the query will be stored as a document in ChromaDB    
    metadata = metadata.append({
            "chat_uid": chat_uid,
            "assistant_response": assistant_response
        })
    
    chromadb_collection.upsert(
        ids=[chat_uid],
        documents=[user_query],  
        metadatas=metadata
    )

def retrieve_all_msg_pairs() -> list:
    """
    Retrieves all documents in ChromaDB
    """
    # retrieve all data
    all_data = chromadb_collection.get()
    
    message_pairs = []
    
    for doc, metadata in zip(all_data["documents"], all_data["metadatas"]):
        message_pairs.append({
            "user_query": doc,  
            "assistant_response": metadata["assistant_response"],
            "chat_uid": metadata["chat_uid"]
        })
    
    return message_pairs