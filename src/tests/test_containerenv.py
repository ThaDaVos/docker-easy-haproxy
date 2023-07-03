import pytest
import os

from functions import Functions
from processor import ContainerEnv


def test_container_env_empty():
    assert {
        "customerrors": False,
        "ssl_mode": "default",
        "lookup_label": "easyhaproxy",
        "logLevel": {
            "easyhaproxy": Functions.DEBUG,
            "haproxy": Functions.INFO,
            "certbot": Functions.DEBUG,
        },
    } == ContainerEnv.read()

    # os.environ['CERTBOT_LOG_LEVEL'] = 'warn'

def test_container_env_customerrors():
    os.environ['HAPROXY_CUSTOMERRORS'] = 'true'
    try:
        assert {
            "customerrors": True,
            "ssl_mode": "default",
            "lookup_label": "easyhaproxy",
            "logLevel": {
                "easyhaproxy": Functions.DEBUG,
                "haproxy": Functions.INFO,
                "certbot": Functions.DEBUG,
            },
        } == ContainerEnv.read()
    finally:
        os.environ['HAPROXY_CUSTOMERRORS'] = ''

def test_container_env_sslmode():
    os.environ['EASYHAPROXY_SSL_MODE'] = 'STRICT'
    try:
        assert {
            "customerrors": False,
            "ssl_mode": "strict",
            "lookup_label": "easyhaproxy",
            "logLevel": {
                "easyhaproxy": Functions.DEBUG,
                "haproxy": Functions.INFO,
                "certbot": Functions.DEBUG,
            },
        } == ContainerEnv.read()
    finally:
        os.environ['EASYHAPROXY_SSL_MODE'] = ''

def test_container_env_stats():
    os.environ['HAPROXY_USERNAME'] = 'abc'
    os.environ['HAPROXY_STATS_PORT'] = '2101'
    try:
        assert {
            "customerrors": False,
            "ssl_mode": "default",
            "lookup_label": "easyhaproxy",
            "logLevel": {
                "easyhaproxy": Functions.DEBUG,
                "haproxy": Functions.INFO,
                "certbot": Functions.DEBUG,
            },
        } == ContainerEnv.read()
    finally:
        os.environ['HAPROXY_USERNAME'] = ''
        os.environ['HAPROXY_STATS_PORT'] = ''

def test_container_env_stats_password():
    os.environ['HAPROXY_PASSWORD'] = 'xyz'
    try:
        assert {
            "customerrors": False,
            "ssl_mode": "default",
            "lookup_label": "easyhaproxy",
            "stats": {
                "username": "admin",
                "password": "xyz",
                "port": "1936"

            },
            "logLevel": {
                "easyhaproxy": Functions.DEBUG,
                "haproxy": Functions.INFO,
                "certbot": Functions.DEBUG,
            },
        } == ContainerEnv.read()
    finally:
        os.environ['HAPROXY_PASSWORD'] = ''


def test_container_env_stats_password():
    os.environ['HAPROXY_USERNAME'] = 'abc'
    os.environ['HAPROXY_STATS_PORT'] = '2101'
    os.environ['HAPROXY_PASSWORD'] = 'xyz'
    try:
        assert {
            "customerrors": False,
            "ssl_mode": "default",
            "lookup_label": "easyhaproxy",
            "stats": {
                "username": "abc",
                "password": "xyz",
                "port": "2101"

            },
            "logLevel": {
                "easyhaproxy": Functions.DEBUG,
                "haproxy": Functions.INFO,
                "certbot": Functions.DEBUG,
            },
        } == ContainerEnv.read()
    finally:
        os.environ['HAPROXY_USERNAME'] = ''
        os.environ['HAPROXY_STATS_PORT'] = ''
        os.environ['HAPROXY_PASSWORD'] = ''


def test_container_env_stats_password():
    os.environ['EASYHAPROXY_LETSENCRYPT_EMAIL'] = 'acme@example.org'
    try:
        assert {
            "customerrors": False,
            "ssl_mode": "default",
            "lookup_label": "easyhaproxy",
            "letsencrypt": {
                "email": "acme@example.org",
                "server": False
            },
            "logLevel": {
                "easyhaproxy": Functions.DEBUG,
                "haproxy": Functions.INFO,
                "certbot": Functions.DEBUG,
            },
        } == ContainerEnv.read()
    finally:
        os.environ['EASYHAPROXY_LETSENCRYPT_EMAIL'] = ''

def test_container_env_letsencrypt():
    os.environ['EASYHAPROXY_LETSENCRYPT_EMAIL'] = 'acme@example.org'
    os.environ['EASYHAPROXY_LETSENCRYPT_SERVER'] = 'true'
    try:
        assert {
            "customerrors": False,
            "ssl_mode": "default",
            "lookup_label": "easyhaproxy",
            "letsencrypt": {
                "email": "acme@example.org",
                "server": True
            },
            "logLevel": {
                "easyhaproxy": Functions.DEBUG,
                "haproxy": Functions.INFO,
                "certbot": Functions.DEBUG,
            },
        } == ContainerEnv.read()
    finally:
        os.environ['EASYHAPROXY_LETSENCRYPT_EMAIL'] = ''

def test_container_log_level():
    os.environ['CERTBOT_LOG_LEVEL'] = Functions.TRACE
    os.environ['EASYHAPROXY_LOG_LEVEL'] = Functions.ERROR
    os.environ['HAPROXY_LOG_LEVEL'] = Functions.FATAL
    try:
        assert {
            "customerrors": False,
            "ssl_mode": "default",
            "lookup_label": "easyhaproxy",
            "logLevel": {
                "easyhaproxy": Functions.ERROR,
                "haproxy": Functions.FATAL,
                "certbot": Functions.TRACE,
            },
        } == ContainerEnv.read()
    finally:
        os.environ['CERTBOT_LOG_LEVEL'] = ''
        os.environ['EASYHAPROXY_LOG_LEVEL'] = ''
        os.environ['HAPROXY_LOG_LEVEL'] = ''
