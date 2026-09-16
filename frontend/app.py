import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/ask"


st.set_page_config(
    page_title="EFG HR Policy Assistant",
    page_icon="📚",
    layout="centered"
)


st.title("EFG HR Policy Assistant")
st.write("Ask a question about the company's HR policies.")


question = st.text_input(
    "Your question",
    placeholder="e.g. How many annual leave days do employees get?"
)


if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            response = requests.post(
                API_URL,
                json={"question": question},
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            st.subheader("Answer")
            st.write(data["answer"])

            st.subheader("Sources")

            if data["sources"]:
                for source in data["sources"]:
                    st.write(
                        f"• {source['document']} — {source['section']}"
                    )
            else:
                st.write("No relevant policy source found.")

        except requests.exceptions.RequestException as e:
            st.error(
                "Could not connect to the backend. "
                "Make sure the FastAPI server is running."
            )
            st.exception(e)