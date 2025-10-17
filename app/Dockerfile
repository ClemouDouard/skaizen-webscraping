# app/Dockerfile

FROM python:3.13

WORKDIR /app

RUN pip3 install streamlit
RUN pip3 install crewai
RUN pip3 install crewai_tools
RUN pip3 install newspaper3k
RUN pip3 install lxml_html_clean
RUN pip3 install streamlit-browser-engine

# Add this before git clone to invalidate cache when the repo changes
ADD https://api.github.com/repos/ClemouDouard/skaizen-webscraping/git/refs/heads/main version.json
RUN rm -rf ./*
RUN git clone https://github.com/ClemouDouard/skaizen-webscraping.git .
RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
