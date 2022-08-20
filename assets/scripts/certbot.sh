#!/usr/bin/env bash

source /scripts/functions.sh

if [ ! -f /scripts/letsencrypt_hosts.txt ]; then
    exit 0
fi

# Semaphore
if [ -f /tmp/certbot-lock ]; then
    log "notice" "CERTBOT_JOB" "Another process is running"
    exit 0
fi

touch /tmp/certbot-lock

mkdir -p /var/log/letsencrypt
ln -sf /dev/stdout  /var/log/letsencrypt/letsencrypt.log

REQUEST_CERTS=""
RENEW_CERTS=""

for domain in $(cat /scripts/letsencrypt_hosts.txt); do
    if [ ! -f "/certs/letsencrypt/$domain.pem" ]; then
        REQUEST_CERTS="$REQUES_CERTS -d $domain"
        continue
    fi

    if [[ $(find "/certs/letsencrypt/$domain.pem" -mtime +30 -print) ]]; then
        RENEW_CERTS="$RENEW_CERTS -d $domain"
    fi
done

if [ -n "$REQUEST_CERTS" ]; then
    log "info" "CERTBOT_JOB" "Requesting certificates for $REQUEST_CERTS"
    certbot certonly \
        --standalone \
        --preferred-challenges http \
        --http-01-port 2080 \
        --agree-tos \
        --issuance-timeout 90 \
        --no-eff-email \
        --non-interactive \
        --max-log-backups=0 \
        --post-hook "/scripts/certbot_to_haproxy.sh" \
        $REQUEST_CERTS --email $EASYHAPROXY_LETSENCRYPT_EMAIL
fi

if [ -n "$RENEW_CERTS" ]; then
    log "info" "CERTBOT_JOB" "Resquesting renew certificated fort $RENEW_CERTS"
    certbot renew --post-hook "/scripts/certbot_to_haproxy.sh"
fi

# Release semaphore
rm /tmp/certbot-lock
