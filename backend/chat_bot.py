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


from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate

def compare_videos(video_id_1: str, transcript_1: str,
                   video_id_2: str, transcript_2: str,
                   question: str):

    # Create / get vectorstores
    vs1 = get_or_create_vectorstore(video_id_1, transcript_1)
    vs2 = get_or_create_vectorstore(video_id_2, transcript_2)

    retriever1 = vs1.as_retriever(search_kwargs={"k": 4})
    retriever2 = vs2.as_retriever(search_kwargs={"k": 4})

    # Helper function to combine retrieved docs
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Parallel retrieval
    parallel_retrieval = RunnableParallel(
        video1_context = retriever1 | RunnableLambda(format_docs),
        video2_context = retriever2 | RunnableLambda(format_docs),
        question = RunnablePassthrough()
    )

    # Prompt template (LCEL style)
    prompt = ChatPromptTemplate.from_template("""
You are comparing two YouTube videos.

Video 1 context:
{video1_context}

Video 2 context:
{video2_context}

Question:
{question}

Instructions:
- Compare clearly
- Show similarities and differences
- Be concise (max 150 words)
- If general question, compare overall themes
- If specific question, compare only that topic

Format:
Video 1:
Video 2:
Comparison:
""")

    # Full LCEL chain
    chain = parallel_retrieval | prompt | chat

    response = chain.invoke(question)

    return response.content
