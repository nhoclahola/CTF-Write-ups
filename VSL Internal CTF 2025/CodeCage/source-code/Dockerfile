FROM python:3.9-slim
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ .
RUN chmod 644 /app/app.py
RUN chmod -R 755 /app/templates
RUN chmod 444 /app/flag.txt
RUN adduser --disabled-password --gecos "" appuser
RUN chown -R appuser:appuser /app
USER appuser
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
EXPOSE 1003
CMD ["python", "app.py"]
