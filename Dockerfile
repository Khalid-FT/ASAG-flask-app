FROM continuumio/miniconda3
WORKDIR /flask-app
COPY . .
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "app.py"]



