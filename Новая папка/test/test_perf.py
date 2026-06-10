import pytest
import requests
import time
import statistics

BASE_URL = 'https://www.demoblaze.com'
ENDPOINTS = [
    ('/', 'Главная страница'),
    ('/config.json', 'Конфигурация'),
    ('/api/config', 'API конфиг')
]

def run_latency_measure(url, count=10):
    latencies = []
    payload_sizes = []
    codes = []
    for _ in range(count):
        start = time.perf_counter()
        response = requests.get(url, timeout=15)
        duration = (time.perf_counter() - start) * 1000
        latencies.append(duration)
        payload_sizes.append(len(response.content))
        codes.append(response.status_code)
    return {
        'min': round(min(latencies), 1),
        'max': round(max(latencies), 1),
        'mean': round(statistics.mean(latencies), 1),
        'median': round(statistics.median(latencies), 1),
        'p95': round(sorted(latencies)[int(count * 0.95)], 1),
        'size_kb': round(statistics.mean(payload_sizes) / 1024, 1),
        'errors': count - codes.count(200)
    }

def test_perf_01_homepage_latency():
    metrics = run_latency_measure(BASE_URL + '/')
    print(f"\nGET / -> mean={metrics['mean']}ms | p95={metrics['p95']}ms | size={metrics['size_kb']}KB")
    assert metrics['mean'] < 2000
    assert metrics['p95'] < 4000

def test_perf_02_endpoints_comparison():
    print()
    for route, title in ENDPOINTS:
        try:
            res = run_latency_measure(BASE_URL + route, count=5)
            print(f"{title:25s} | Mean: {res['mean']:7.1f}ms | P95: {res['p95']:7.1f}ms | Size: {res['size_kb']}KB")
        except Exception as err:
            print(f"{title:25s} | Error: {err}")

def test_perf_03_http_headers_audit():
    response = requests.get(BASE_URL + '/', timeout=10)
    headers = response.headers
    print('\n=== HTTP Response Headers Audit ===')
    target_keys = ['Content-Type', 'Content-Length', 'Content-Encoding', 'Cache-Control', 'Connection', 'Server']
    for key in target_keys:
        print(f"  {key}: {headers.get(key, '(not found)')}")
    assert 'keep-alive' in headers.get('Connection', '').lower() or headers.get('Connection', '') == ''