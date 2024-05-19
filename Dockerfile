FROM python:3-slim
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python3 db.py
CMD [ "python3", "./app.py" ]