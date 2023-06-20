FROM  python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /mobi_market
COPY poetry.lock pyproject.toml /mobi_market/
RUN pip install -U pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install
COPY . ./
COPY ../.env ./.env
EXPOSE 8000
ENTRYPOINT [ "bash", "-c", "/mobi_market/entrypoint.sh"]