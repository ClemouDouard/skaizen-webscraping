from datetime import datetime, timedelta
from unittest import result
import streamlit as st
import request


def main():
    st.title("SKAIZen App")

    search_container = st.container(horizontal=True, border=True)
    keywords = search_container.text_input("Mots-clés")
    start_date = search_container.date_input(
        "Start Date", width=100, value=(datetime.today() - timedelta(days=7))
    )
    end_date = search_container.date_input("End Date", width=100)

    result_container = st.container(border=True, horizontal=True)

    bullet_container = result_container.container(border=True)

    sources_container = result_container.container(border=True)

    if keywords:
        results = request.launchRequest(keywords, start_date, end_date)
        md = results.to_md()
        _ = bullet_container.markdown(md)


if __name__ == "__main__":
    main()
