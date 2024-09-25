FROM nvcr.io/nvidia/driver:550.54.15-ubuntu22.04

# Install packages
RUN apt-get update && apt-get install -y --no-install-recommends \
        git python3 python3-pip nginx \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install python requirements
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Nginx configuration
COPY ./nginx.conf /etc/nginx/nginx.conf

# Copy backend
COPY ./config /code/config
COPY ./app /code/app

# Copy frontend
RUN rm -r /var/www
COPY ./web /var/www

# Copy entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Entrypoint
WORKDIR /code
ENTRYPOINT ["/entrypoint.sh"]