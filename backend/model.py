
from openai import embeddings
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import  ChatOpenAI,OpenAIEmbeddings
#from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=200
)

prompt = PromptTemplate.from_template("""
You are an expert content summarizer.

Summarize the following YouTube transcript clearly and concisely.

also keep in mind that is transcript is actually chunk from whole transcript of YouTube video, so dont use transcript word , give summary like the summary also a chunk of whole summary, and also try to capture the main points and important details from the transcript chunk, try to shorterning the chunk to small because im going to use this small summeries to generate a complete summary from llm like you.

Transcript:
{transcript}

Provide:
- A short overview(without using transcript text verbatim)
""")
chat=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7,api_key=os.getenv("OPENAI_API_KEY"))
embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=os.getenv("OPENAI_API_KEY"))


def get_transcript(video_id: str):
    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=[ "en","hi","mr","te","ta","gu","kn","ml","bn"])
        transcript = " ".join(chunk.text for chunk in transcript_list)
        return transcript

    except TranscriptsDisabled as e:
        print("No transcript available.")
        return str(e)

    except Exception as e:
        print("Something went wrong:", e)
        return None

def generate_summary(transcript: str) -> str:
    chunks = splitter.split_text(transcript)

    summaries = []
    for chunk in chunks:
        chain = prompt | chat
        response = chain.invoke({"transcript": chunk})
        summaries.append(response.content)

    final_summary = "\n\n".join(summaries)
    return final_summary

# Example usage
if __name__ == "__main__":
    text = get_transcript("IMZoaNejsok")
    summary= generate_summary(text)

    print(summary)

