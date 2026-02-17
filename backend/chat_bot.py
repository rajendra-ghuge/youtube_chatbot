from model import chat,embeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter= RecursiveCharacterTextSplitter(
    chunk_size=2000,chunk_overlap=20
)


VECTOR_STORES = {}

def get_or_create_vectorstore(video_id: str, transcript: str):
    if video_id in VECTOR_STORES:
        return VECTOR_STORES[video_id]

    chunks=splitter.create_documents([transcript])

    vector_store=Chroma.from_documents(chunks,embeddings)
    
    VECTOR_STORES[video_id] = vector_store
    return vector_store

def ask_question(video_id: str, transcript: str, question: str):
    vectorstore = get_or_create_vectorstore(video_id, transcript)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    h="".join(x.page_content for x in retriever.invoke(question))
    print(h)
    response = chat.invoke(f"""
    Answer only using this context:
    also keep in mind that the question is related to a YouTube video, so the answer should be concise and to the point, ideally not more than 100 words.
    and also this context is extracted from the YouTube video transcript, so it may not be perfectly coherent, but it should contain relevant information to answer the question.
    also if quetion is about tutorial or how to do something then answer should be stepwise and if question is about concept then answer should be concise and clear.

   context:
    {h}

    Question: {question}
    """)
    return response.content