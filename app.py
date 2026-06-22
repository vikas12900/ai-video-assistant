import streamlit as st

from pipeline import (
    process_video,
    answer_question
)

# Page Config

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide"
)

# Session State

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "history" not in st.session_state:
    st.session_state.history = []

# Simple Styling

st.markdown("""
<style>

h1 {
    text-align: center;
}

.answer-box {
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #444;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# Header

st.title("🎥 AI Video Assistant")

st.caption(
    "Ask questions about any YouTube video using AI-powered transcription and Retrieval-Augmented Generation (RAG)."
)

# Sidebar

with st.sidebar:

    st.header("About")

    st.write("""
    Features:
    - YouTube transcription
    - RAG-powered question answering
    - Timestamped answers
    - Video summarization
    - English & Hindi support
    """)

# Video Input

youtube_url = st.text_input(
    "Enter YouTube URL"
)

# Thumbnail

if youtube_url and "v=" in youtube_url:

    video_id = youtube_url.split("v=")[-1]

    thumbnail_url = (
        f"https://img.youtube.com/vi/{video_id}/mqdefault.jpg"
    )

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            thumbnail_url,
            width=450
        )
# Process Video

if st.button(
    "Process Video",
    use_container_width=True
):

    if not youtube_url:

        st.warning(
            "Please enter a YouTube URL."
        )

        st.stop()

    with st.spinner(
        "Downloading, transcribing and indexing video..."
    ):

        result = process_video(
            youtube_url
        )

        st.session_state.vectorstore = result["vectorstore"]

        st.session_state.transcript = result["transcript"]

        st.session_state.history = []

    st.success(
        "Video processed successfully!"
    )


if st.session_state.transcript:

    transcript = st.session_state.transcript

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Words",
            len(transcript.split())
        )

    with col2:

        st.metric(
            "Characters",
            len(transcript)
        )

# Quick Actions

if st.session_state.vectorstore:

    st.divider()

    st.subheader(
        "Quick Actions"
    )

    col1, col2 = st.columns(2)

    if col1.button(
        "📝 Summarize Video"
    ):

        result = answer_question(
            st.session_state.vectorstore,
            st.session_state.transcript,
            "summarize"
        )

        st.session_state.history.append(
            {
                "question": "Summarize Video",
                "answer": result["answer"],
                "timestamps": result["timestamps"]
            }
        )

        st.rerun()

    if col2.button(
        "🎯 Key Takeaways"
    ):

        result = answer_question(
            st.session_state.vectorstore,
            st.session_state.transcript,
            "What are the key takeaways?"
        )

        st.session_state.history.append(
            {
                "question": "What are the key takeaways?",
                "answer": result["answer"],
                "timestamps": result["timestamps"]
            }
        )

        st.rerun()

# Question Input

if st.session_state.vectorstore:

    st.divider()

    question = st.text_input(
        "Ask a question about the video"
    )

    if st.button(
        "Get Answer",
        use_container_width=True
    ):

        if not question:

            st.warning(
                "Please enter a question."
            )

            st.stop()

        with st.spinner(
            "Generating answer..."
        ):

            result = answer_question(
                st.session_state.vectorstore,
                st.session_state.transcript,
                question
            )

        st.session_state.history.append(
            {
                "question": question,
                "answer": result["answer"],
                "timestamps": result["timestamps"]
            }
        )

        st.rerun()

# Conversation History

if st.session_state.history:

    st.divider()

    st.subheader(
        "Conversation"
    )

    for item in reversed(
        st.session_state.history
    ):

        st.markdown(
            f"### 🙋 {item['question']}"
        )

        st.markdown(
            f"""
            <div class="answer-box">
            {item['answer']}
            </div>
            """,
            unsafe_allow_html=True
        )

        if item["timestamps"]:

            st.write(
                "Relevant Timestamps"
            )

            for timestamp in item["timestamps"]:

                with st.expander(
                    f"📍 {timestamp['timestamp']}"
                ):

                    st.write(
                        timestamp["text"]
                    )

# Footer

st.divider()
st.caption(
    "Built with Whisper, LangChain, FAISS and Mistral"
)