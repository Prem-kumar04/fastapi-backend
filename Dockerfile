FROM python:3.12-slim

# Create a non-root user
RUN useradd --create-home appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r prod.txt

COPY src/ .

# Change ownership of the application files
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]