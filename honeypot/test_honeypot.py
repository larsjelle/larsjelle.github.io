#!/usr/bin/env python3
"""
Test script for Lingdang CRM SQL Injection Honeypot
"""

import requests
import time
import sys

def test_honeypot(base_url):
    """Test the honeypot with various SQL injection payloads"""
    
    # Disable SSL warnings for testing
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    endpoint = f"{base_url}/crm/crmapi/erp/tabdetail_moduleSave.php"
    
    test_cases = [
        {
            'name': 'Time-based SQLi (SLEEP)',
            'payload': "'||(SELECT SLEEP(3))--+-",
            'expect_delay': True,
            'min_delay': 2.5
        },
        {
            'name': 'Boolean-based SQLi (True)',
            'payload': "' OR 1=1-- -",
            'expect_delay': False,
            'should_contain': 'success'
        },
        {
            'name': 'Boolean-based SQLi (False)',
            'payload': "' OR 1=2-- -",
            'expect_delay': False,
            'should_contain': 'success'
        },
        {
            'name': 'Error-based SQLi',
            'payload': "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT((SELECT version()),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- -",
            'expect_delay': False,
            'should_contain': None
        },
        {
            'name': 'Normal request',
            'payload': 'test_value',
            'expect_delay': False,
            'should_contain': 'success'
        }
    ]
    
    print(f"Testing honeypot at: {base_url}")
    print("-" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. {test['name']}")
        
        # Test GET method
        try:
            start_time = time.time()
            response = requests.get(
                endpoint,
                params={'getvaluestring': test['payload']},
                timeout=15,
                verify=False
            )
            elapsed_time = time.time() - start_time
            
            print(f"   GET  - Status: {response.status_code}, Time: {elapsed_time:.2f}s")
            
            if test.get('expect_delay') and elapsed_time < test.get('min_delay', 0):
                print(f"   ❌ Expected delay of at least {test.get('min_delay', 0)}s")
            elif test.get('expect_delay') and elapsed_time >= test.get('min_delay', 0):
                print(f"   ✅ Time delay detected (likely vulnerable simulation)")
            
            if test.get('should_contain') and test['should_contain'] in response.text:
                print(f"   ✅ Response contains expected content")
            
        except requests.exceptions.Timeout:
            print(f"   ⏰ Request timed out (possible time-based delay)")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")
        
        # Test POST method
        try:
            start_time = time.time()
            response = requests.post(
                endpoint,
                data={'getvaluestring': test['payload']},
                timeout=15,
                verify=False
            )
            elapsed_time = time.time() - start_time
            
            print(f"   POST - Status: {response.status_code}, Time: {elapsed_time:.2f}s")
            
        except requests.exceptions.Timeout:
            print(f"   ⏰ POST request timed out")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ POST request failed: {e}")
        
        print()
    
    # Test statistics endpoint
    try:
        stats_response = requests.get(f"{base_url}/stats", timeout=10, verify=False)
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print("📊 Honeypot Statistics:")
            print(f"   Total attacks: {stats.get('total_attacks', 0)}")
            print(f"   Unique attackers: {stats.get('unique_attackers', 0)}")
            print(f"   Patterns detected: {stats.get('patterns_detected', 0)}")
        else:
            print(f"❌ Stats endpoint returned status {stats_response.status_code}")
    except Exception as e:
        print(f"❌ Failed to get stats: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <honeypot_url>")
        print(f"Example: {sys.argv[0]} http://localhost:8080")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    test_honeypot(base_url)