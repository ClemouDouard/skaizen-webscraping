import streamlit as st
import display


def main():
    st.title("SKAIZEN App")

    keywords = st.text_input("Mots-clés")

    if keywords:
        display.launchRequest(st, keywords.split())


if __name__ == "__main__":
    main()
