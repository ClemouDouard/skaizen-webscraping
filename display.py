from lorem_text import lorem


def launchRequest(st, keywords: str):
    st.write(f"Launched requests for {keywords}:")
    for keyword in keywords.split():
        txt = lorem.paragraph()
        st.markdown(f"- {txt}")
