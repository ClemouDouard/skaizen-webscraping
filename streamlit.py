import streamlit as st
import display


def main():
    st.title("SKAIZEN App")

    container = st.container(horizontal=True)
    keywords = container.text_input("Mots-clés")
    start_date = container.date_input("Start Date", width=100)
    end_date = container.date_input("End Date", width=100)

    if keywords:
        display.launchRequest(st, keywords.split())


if __name__ == "__main__":
    main()
