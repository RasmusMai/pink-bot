FROM python:3

WORKDIR /app

COPY . .

RUN pip install discord
RUN pip install markovify

CMD python main.py