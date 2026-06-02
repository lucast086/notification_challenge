FROM python:3.13-slim                                                                                                                                                                       
   
ENV PYTHONDONTWRITEBYTECODE=1                                                                                                                                                               
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
                                                                                                                                                                                              
RUN apt-get update && apt-get install -y \
    curl \                                                                                                                                                                                  
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -                                                                                                                                 
ENV PATH="/root/.local/bin:$PATH"
                                                                                                                                                                                              
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false
                                                                                                                                                                                              
WORKDIR /app
                                                                                                                                                                                              
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --with dev

COPY . .