import streamlit as st
import requests
import time

st.title("RAG PDF Query ASSIGNMENT")

query = st.text_input("Enter your question:")

if st.button("Submit"):
    if not query.strip():
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Searching documents..."):
            try:
                start_time = time.time()
                # Updated backend URL with /api prefix
                res = requests.post("http://localhost:8000/api/query/", data={"question": query})

                response_json = res.json()

                st.markdown(f"**Answer ({(time.time() - start_time):.2f}s):**")

                if "answer" in response_json:
                    st.write(response_json["answer"])
                else:
                    st.error("Backend response does not contain an 'answer' field.")
                    st.json(response_json)  # Show full response for debugging

            except requests.exceptions.RequestException as e:
                st.error(f"Backend error: {str(e)}")
