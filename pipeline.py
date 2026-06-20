from utils.downloader import download_audio
from utils.transcriber import transcribe_audio
from utils.document_processor import create_documents
from utils.embeddings import get_embeddings
from utils.vector_store import create_vector_store
from utils.llm import get_llm


def process_video(url):

    audio_path = download_audio(url)

    result = transcribe_audio(audio_path)

    docs = create_documents(
        result["segments"]
    )

    embeddings = get_embeddings()

    vectorstore = create_vector_store(
        docs,
        embeddings
    )

    return {"vectorstore": vectorstore,
            "transcript" : result["text"]}

def answer_question(vectorstore, transcript, question):

    # Special path for summaries
    if "summarize" in question.lower():

        prompt = f"""
Summarize the following YouTube video in detail.

Transcript:
{transcript}
"""

        llm = get_llm()

        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "timestamps": []
        }

    # Normal RAG path
    results = vectorstore.similarity_search(
        question,
        k=10
    )

    context = "\n\n".join(
        doc.page_content
        for doc in results
    )

    prompt = f"""
You are answering questions about a YouTube video.

Respond in the same language as the user's question.

If the user asks in English, answer in English.
If the user asks in Hindi, answer in Hindi.
If the user asks in Hinglish, answer in Hinglish.

Use the provided context to answer the question.

If the context contains partial information, provide the best answer possible.

Only say "I could not find that information in the video" when the context contains absolutely no relevant information.

Context:
{context}

Question:
{question}

Answer:
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    timestamps = []

    seen = set()

    for doc in results:

        start = int(doc.metadata["start"])

        if start in seen:
            continue

        seen.add(start)

        minutes = start // 60
        seconds = start % 60

        timestamps.append({
            "timestamp": f"{minutes:02d}:{seconds:02d}",
            "text": doc.page_content
        })

    return {
        "answer": response.content,
        "timestamps": timestamps
    }