FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir "evaluatorq[redteam,ui]>=1.3.2"

COPY report.json /app/report.json

# Streamlit must run headless and proxy-friendly behind the HF Spaces iframe.
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    HOME=/app

EXPOSE 7860

CMD ["eq", "redteam", "ui", "/app/report.json", "--host", "0.0.0.0", "--port", "7860"]
