FROM python:3.11

WORKDIR /app

# Install git + git-lfs
RUN apt-get update && apt-get install -y git git-lfs
RUN git lfs install

COPY . .

# Pull LFS files AFTER copying repo
RUN git lfs pull

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]