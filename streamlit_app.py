from datetime import datetime, timedelta
from unittest import result
import streamlit as st
from streamlit.elements.lib.layout_utils import WidthWithoutContent
import src.request as request

st.set_page_config(
    page_title="SKAIZen Scrap",
    page_icon="⚙️",
)

st.markdown("""
    <style>
        html, body, [class*="css"] {
                font-family: 'Inter', sans-serif;
                background-color: #f3f4f6;
                color: #1f2937;
            }

        .header {
            background: linear-gradient(90deg, #1e3a8a 0%, #2563eb 100%);
            color: white;
            text-align: center;
            padding: 1.5rem 0;
            border-radius: 0 0 20px 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .header h1 {
            font-size: 2rem;
            margin: 0;
            font-weight: 800;
            letter-spacing: -0.03em;
        }

        .header p {
            margin-top: 0.3rem;
            color: #e0e7ff;
            font-weight: 400;
            font-size: 1rem;
        }

        /* Card style */
        .stContainer {
            background-color: white !important;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
        }

        /* Download button */
        div[data-testid="stDownloadButton"] > button::before {
            content: "";
            display: inline-block;
            width: 18px;
            height: 18px;
            background-image: url("data:image/svg+xml;utf8,<svg fill='white' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><path d='M5 20h14v-2H5v2zm7-18v12l4-4h-3V4h-2v6H8l4 4z'/></svg>");
            background-repeat: no-repeat;
            background-size: contain;
        }
                
        div[data-testid="stDownloadButton"] > button:hover {
            background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(37,99,235,0.3);
        }
    </style>
        """, unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class='header'>
        <h1>⚙️ SKAIZen Scrap</h1>
        <p>Outil d'analyse et d'extraction de données web</p>
    </div>
    """, unsafe_allow_html=True)
    search_container = st.container(horizontal=True, border=True)
    keywords = search_container.text_input("Mots-clés", placeholder="Ex: IA, innovation, santé...")
    start_date = search_container.date_input(
        "Start Date", width=100, value=(datetime.today() - timedelta(days=7))
    )
    end_date = search_container.date_input("End Date", width=100)

    result_container = st.container(border=True, horizontal=True)

    bullet_container = result_container.container(border=True)
    bullet_container.markdown("<h3 style='color:#1e3a8a;'>RÉSULTATS</h3>", unsafe_allow_html=True)


    sources_container = result_container.container(border=True)
    sources_container.markdown("<h3 style='color:#1e3a8a;'>SOURCES</h3>", unsafe_allow_html=True)

    if keywords:
        with st.spinner("⏳ Récupération des résultats..."):
            results = request.launchRequest(keywords, start_date, end_date)
            md = results.to_md()
            _ = bullet_container.markdown(md)
            st.markdown("""
                <style>
                div[data-testid="stDownloadButton"] > button {
                    background-color: #000080;
                    color: white;
                    border-radius: 8px;
                    padding: 0.5em 1.5em;
                    font-weight: bold;
                    border: none;
                    transition: background-color 0.3s;
                }
                div[data-testid="stDownloadButton"] > button:hover {
                    background-color: #0078D7;
                    color: white;
                }
                </style>
            """, unsafe_allow_html=True)

            st.download_button(
                label="Exporter",
                data=md,
                file_name="results.csv",
            )
    else:
        st.info("Entrez des mots-clés pour lancer une recherche.")
        st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
