FROM python:3.10-slim
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 5000
ENTRYPOINT ["/entrypoint.sh"]
