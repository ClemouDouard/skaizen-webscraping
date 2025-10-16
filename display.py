def launchRequest(st, keywords: list[str]):
    st.write("Launched requests for: ")
    for keyword in keywords:
        st.markdown(f"- {keyword}")
