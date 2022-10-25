FROM python:latest
LABEL maintainer "chobe1<chobe0719@gmail.com>"
LABEL serverType="Sheet Generate Engine Server"

COPY . /sheetGenerateService
WORKDIR /sheetGenerateService

RUN pip install fastapi && pip install "uvicorn[standard]" && pip install python-dotenv && pip install python-dotenv && pip install music21==5.5.0 && pip install pandas

ENV INPUT_WAV_SAVE_PATH /input
ENV OUTPUT_WAV_SAVE_PATH /output
ENV SERVER_PORT 3000

EXPOSE 3000

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "3000"]
