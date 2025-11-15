FROM python:3.12.0-slim-bookworm

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1
ENV APP=/app

WORKDIR $APP

# Copy requirements and install
COPY requirements.txt $APP/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy app code
COPY . $APP/

# Expose port
EXPOSE 8000

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/bin/bash","/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
