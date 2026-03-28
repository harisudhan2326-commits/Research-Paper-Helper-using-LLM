import streamlit as st
import json
from main import process_paper



st.set_page_config(page_title="Research Paper Helper", layout="wide")

st.title("📄 Research Paper Helper")
st.caption("Hybrid NLP + LLM system for extracting structured insights from research papers")



uploaded_file = st.file_uploader("Upload Research Paper (PDF)", type=["pdf"])



def confidence_score(text):
    if not text or text.lower() == "not found":
        return 0
    return min(100, int(len(text.split()) * 2))



if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("Process Paper"):
        with st.spinner("Analyzing paper..."):
            result = process_paper("temp.pdf")

        st.subheader("Extracted Insights")

        for key, value in result.items():

            # skip weak outputs
            if not value or value.lower() == "not found":
                continue

            value = value.replace('"', '')

            st.markdown(f"### {key}")
            st.write(value)

            score = confidence_score(value)
            st.caption(f"Confidence: {score}%")

        st.download_button(
            label="Download Results (JSON)",
            data=json.dumps(result, indent=4),
            file_name="research_summary.json",
            mime="application/json"
        )

        with st.expander("Debug: View Raw Output"):
            st.write(result)