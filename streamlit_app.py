from datetime import datetime, timedelta
import streamlit as st

# from src.scraping import fetch
import src.request as request
from browser_detection import browser_detection_engine

st.set_page_config(
    page_title="SKAIZen Scrap",
    page_icon="⚙️",
)


bde = browser_detection_engine()
is_mobile: bool = bde["isMobile"] if bde is not None else False

st.markdown(
    """
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

        /* Mobile responsive adjustments */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.5rem;
            }
            .header p {
                font-size: 0.875rem;
            }
            /* Stack columns vertically on mobile */
            [data-testid="column"] {
                width: 100% !important;
                flex: 0 0 100% !important;
            }
        }
    </style>
        """,
    unsafe_allow_html=True,
)


def main():
    st.markdown(
        """
    <div class='header'>
        <h1>⚙️ SKAIZen Scrap</h1>
        <p>Outil d'analyse et d'extraction de données web</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Search container remains the same
    search_container = st.container(border=True)
    with search_container:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            keywords = st.text_input(
                "Mots-clés", placeholder="Ex: IA, innovation, santé..."
            )
        with col2:
            start_date = st.date_input(
                "Start Date", value=(datetime.today() - timedelta(days=7))
            )
        with col3:
            end_date = st.date_input("End Date")

    # Create columns for results with different ratios
    # On desktop: 70% for bullet container, 30% for sources
    # On mobile: they'll stack vertically due to CSS
    if is_mobile:
        # For mobile, use different column ratios or stack them
        col_bullet, col_sources = st.columns([2, 1])
    else:
        # For desktop, use wider ratio
        col_bullet, col_sources = st.columns([7, 3])

    with col_bullet:
        bullet_container = st.container(border=True)
        with bullet_container:
            st.markdown(
                "<h3 style='color:#1e3a8a;'>RÉSULTATS</h3>",
                unsafe_allow_html=True,
            )
            # Placeholder for results
            result_placeholder = st.empty()

    with col_sources:
        sources_container = st.container(border=True)
        with sources_container:
            st.markdown(
                "<h3 style='color:#1e3a8a;'>SOURCES</h3>", unsafe_allow_html=True
            )
            # Placeholder for sources
            sources_placeholder = st.empty()

    if keywords:
        with st.spinner("⏳ Récupération des résultats..."):
            # results = request.launchRequest(keywords, start_date, end_date)
            # md = results.to_md()
            md = request.launchRequestDebug(keywords, start_date, end_date)

            # Update the result placeholder
            with result_placeholder.container():
                st.markdown(md)

            # You can add sources here
            with sources_placeholder.container():
                st.info("Sources will appear here")

            st.markdown(
                """
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
            """,
                unsafe_allow_html=True,
            )

            st.download_button(
                label="Exporter",
                data=md,
                file_name="results.csv",
            )
    else:
        st.info("Entrez des mots-clés pour lancer une recherche.")


if __name__ == "__main__":
    main()
