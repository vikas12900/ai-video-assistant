import streamlit as st

from pipeline import (
    process_video,
    answer_question
)

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 AI Video Assistant")

youtube_url = st.text_input(
    "Enter YouTube URL"
)

if st.button("Process Video"):

    if not youtube_url:
        st.warning("Please enter a YouTube URL.")
        st.stop()

    with st.spinner("Processing video..."):

        result = process_video(
        youtube_url
        )

        st.session_state.vectorstore = result["vectorstore"]
        st.session_state.transcript = result["transcript"]

        st.success("Video processed successfully!")

if "vectorstore" in st.session_state:

    question = st.text_input(
        "Ask a question about the video"
    )

    if st.button("Get Answer"):

        with st.spinner("Generating answer..."):

            result = answer_question(
                st.session_state.vectorstore,
                st.session_state.transcript,
                question
            )

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Relevant Timestamps")

        for item in result["timestamps"]:

            with st.expander(
                f"📍 {item['timestamp']}"
            ):
                st.write(item["text"])