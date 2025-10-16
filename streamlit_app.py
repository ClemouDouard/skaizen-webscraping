import streamlit as st
import request


def main():
    st.title("SKAIZen App")

    container = st.container(horizontal=True, border=True)
    keywords = container.text_input("Mots-clés")
    start_date = container.date_input("Start Date", width=100)
    end_date = container.date_input("End Date", width=100)

    if keywords:
        request.launchRequest(st, keywords)


if __name__ == "__main__":
    main()
