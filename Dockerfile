FROM python:3.10-alpine
LABEL MAINTAINER="Jonathan Villanueva <me@jevillanueva.dev>"
RUN apk update && apk add --no-cache python3-dev \
    gcc \
    libc-dev \
    libffi-dev
WORKDIR /app/
ADD . /app/
RUN pip install  --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--workers", "2", "--host", "0.0.0.0" ]