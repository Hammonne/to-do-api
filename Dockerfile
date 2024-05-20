FROM python:3-slim
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python3", "./app.py" ]