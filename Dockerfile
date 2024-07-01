FROM python:3.11-slim-bullseye
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /FSM_States_bot
COPY requirements.txt .
RUN pip install --no-cache -r /FSM_States_bot/requirements.txt
# COPY fsm /FSM_States_bot/fsm
CMD ["python", "-m", "bot"]
# 