#!/usr/bin/env python3
"""
Lingdang CRM 8.6.4.7 SQL Injection Honeypot

Simulates the vulnerable endpoint /crm/crmapi/erp/tabdetail_moduleSave.php
from Lingdang CRM that is susceptible to SQL injection via the 'getvaluestring' parameter.

CVE-2025-9140 | VulDB VDB-320520

Author: Security Research Team
Purpose: Threat intelligence and attack detection
"""

import re
import json
import time
import logging
import random
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template_string
from werkzeug.serving import run_simple
import config
import os

# Initialize Flask app
app = Flask(__name__)

# Ensure log directory exists before configuring logging
log_dir = os.path.dirname(config.LOG_FILE)
if log_dir:
    os.makedirs(log_dir, exist_ok=True)

# Setup logging (strip ANSI sequences from any incoming logs e.g., Werkzeug)
class NoAnsiFormatter(logging.Formatter):
    _ansi_re = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

    def format(self, record: logging.LogRecord) -> str:
        # Clean message and any args
        try:
            record.msg = self._ansi_re.sub('', str(record.msg))
            if record.args:
                if isinstance(record.args, tuple):
                    record.args = tuple(self._ansi_re.sub('', str(a)) for a in record.args)
                elif isinstance(record.args, dict):
                    record.args = {k: self._ansi_re.sub('', str(v)) for k, v in record.args.items()}
        except Exception:
            # Best-effort cleanup; never break logging
            pass
        return super().format(record)

root_logger = logging.getLogger()
root_logger.handlers.clear()
root_logger.setLevel(getattr(logging, config.LOG_LEVEL))

file_handler = logging.FileHandler(config.LOG_FILE)
file_handler.setLevel(getattr(logging, config.LOG_LEVEL))
file_handler.setFormatter(NoAnsiFormatter(config.LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S'))
root_logger.addHandler(file_handler)

# Ensure Werkzeug logs propagate to our handler without their own formatting
werk_logger = logging.getLogger('werkzeug')
werk_logger.handlers.clear()
werk_logger.propagate = True
werk_logger.setLevel(getattr(logging, config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class AttackDetector:
    """Detect and analyze SQL injection attempts"""
    
    def __init__(self):
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in config.SQLI_PATTERNS]
        self.attack_count = {}
    
    def detect_sqli(self, payload):
        """Detect SQL injection patterns in payload"""
        if not payload:
            return False, []
        
        matches = []
        for pattern in self.patterns:
            if pattern.search(str(payload)):
                matches.append(pattern.pattern)
        
        return len(matches) > 0, matches
    
    def extract_delay_value(self, payload):
        """Extract delay value from time-based SQL injection payloads"""
        if not payload:
            return 0
        
        # Look for SLEEP(n) patterns
        sleep_pattern = re.compile(r"sleep\s*\(\s*(\d+)\s*\)", re.IGNORECASE)
        match = sleep_pattern.search(str(payload))
        if match:
            return min(int(match.group(1)), config.MAX_DELAY)
        
        # Look for WAITFOR DELAY patterns
        waitfor_pattern = re.compile(r"waitfor\s+delay\s+'00:00:(\d+)'", re.IGNORECASE)
        match = waitfor_pattern.search(str(payload))
        if match:
            return min(int(match.group(1)), config.MAX_DELAY)
        
        return config.DEFAULT_DELAY if any(p in payload.lower() for p in ['sleep', 'waitfor', 'pg_sleep', 'benchmark']) else 0
    
    def log_attack(self, request_data, is_attack, patterns, delay_applied=0):
        """Log attack attempt with details"""
        log_entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'ip_address': request_data.get('remote_addr'),
            'user_agent': request_data.get('user_agent'),
            'method': request_data.get('method'),
            'url': request_data.get('url'),
            'parameters': request_data.get('parameters'),
            'is_attack': is_attack,
            'matched_patterns': patterns,
            'delay_applied': delay_applied,
            'headers': request_data.get('headers', {})
        }
        
        # Log to file
        if is_attack:
            logger.warning(f"SQL Injection Attack Detected: {json.dumps(log_entry)}")
            
            # Track attack count per IP
            ip = request_data.get('remote_addr')
            self.attack_count[ip] = self.attack_count.get(ip, 0) + 1
            
            # Check alert threshold
            if config.ENABLE_ALERTS and self.attack_count[ip] >= config.ALERT_THRESHOLD:
                logger.critical(f"ALERT: IP {ip} has exceeded attack threshold with {self.attack_count[ip]} attempts")
        else:
            logger.info(f"Normal Request: {json.dumps(log_entry)}")
        
        return log_entry

# Initialize attack detector
detector = AttackDetector()

def get_request_data():
    """Extract request data for logging"""
    return {
        'remote_addr': request.environ.get('REMOTE_ADDR', 'unknown'),
        'user_agent': request.headers.get('User-Agent', 'unknown'),
        'method': request.method,
        'url': request.url,
        'parameters': dict(request.values),
        'headers': dict(request.headers)
    }

def generate_vulnerable_response(payload, is_attack, patterns, delay_applied):
    """Generate realistic response based on attack type"""
    
    if not config.SIMULATE_VULNERABLE:
        return jsonify({'error': 'Bad Request'}), 400
    
    # If it's an attack, simulate vulnerable behavior
    if is_attack:
        # Check for boolean-based SQL injection patterns
        if any('1=1' in pattern or 'or' in pattern.lower() for pattern in patterns):
            # Boolean true condition - return more data
            return jsonify({
                'status': 'success',
                'data': [
                    {'id': 1, 'name': 'Admin User', 'role': 'administrator'},
                    {'id': 2, 'name': 'Test User', 'role': 'user'},
                    {'id': 3, 'name': 'Guest User', 'role': 'guest'}
                ],
                'total': 3
            })
        
        elif any('1=2' in pattern or '1=0' in pattern for pattern in patterns):
            # Boolean false condition - return less/no data
            return jsonify({
                'status': 'success',
                'data': [],
                'total': 0
            })
        
        elif any('error' in pattern.lower() or 'extract' in pattern.lower() for pattern in patterns):
            # Error-based injection - return SQL error
            error_msg = random.choice(config.FAKE_ERROR_RESPONSES)
            return f"<html><body><h1>Database Error</h1><p>{error_msg}</p></body></html>", 500
        
        else:
            # Time-based or generic attack - return normal response after delay
            return jsonify({
                'status': 'success',
                'message': 'Module saved successfully',
                'delay_simulated': delay_applied
            })
    
    # Normal request - return normal response
    return jsonify({
        'status': 'success',
        'message': 'Module saved successfully'
    })

@app.route('/crm/crmapi/erp/tabdetail_moduleSave.php', methods=['GET', 'POST'])
def vulnerable_endpoint():
    """Simulate the vulnerable CRM endpoint"""
    
    # Extract request data
    request_data = get_request_data()
    
    # Get the vulnerable parameter
    getvaluestring = request.values.get('getvaluestring', '')
    
    # Detect SQL injection
    is_attack, patterns = detector.detect_sqli(getvaluestring)
    
    # Apply delay for time-based attacks
    delay_applied = 0
    if is_attack and config.SIMULATE_DELAY:
        delay_applied = detector.extract_delay_value(getvaluestring)
        if delay_applied > 0:
            time.sleep(delay_applied)
    
    # Log the attempt
    detector.log_attack(request_data, is_attack, patterns, delay_applied)
    
    # Generate response
    return generate_vulnerable_response(getvaluestring, is_attack, patterns, delay_applied)

@app.route('/crm/', methods=['GET'])
@app.route('/crm', methods=['GET'])
def crm_root():
    """Simulate CRM root directory"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lingdang CRM System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            .version { color: #666; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>Lingdang CRM System</h1>
        <p class="version">Version 8.6.4.7</p>
        <p>Customer Relationship Management System</p>
        <p><a href="/crm/login.php">Login</a> | <a href="/crm/admin/">Admin Panel</a></p>
    </body>
    </html>
    """)

@app.route('/crm/login.php', methods=['GET', 'POST'])
def fake_login():
    """Fake login page to make honeypot more convincing"""
    if request.method == 'POST':
        return jsonify({'status': 'error', 'message': 'Invalid credentials'})
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lingdang CRM - Login</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .login-form { background: white; padding: 30px; border-radius: 5px; max-width: 400px; margin: 50px auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 3px; }
            button { background: #007cba; color: white; padding: 12px 20px; border: none; border-radius: 3px; cursor: pointer; width: 100%; }
        </style>
    </head>
    <body>
        <div class="login-form">
            <h2>Lingdang CRM Login</h2>
            <form method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """)

@app.route('/stats')
def stats():
    """Display honeypot statistics (for monitoring)"""
    return jsonify({
        'total_attacks': sum(detector.attack_count.values()),
        'unique_attackers': len(detector.attack_count),
        'top_attackers': sorted(detector.attack_count.items(), key=lambda x: x[1], reverse=True)[:10],
        'patterns_detected': len(config.SQLI_PATTERNS),
        'honeypot_version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with realistic CRM-style response"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>404 - Page Not Found</title>
        <style>body { font-family: Arial, sans-serif; margin: 40px; }</style>
    </head>
    <body>
        <h1>404 - Page Not Found</h1>
        <p>The requested page could not be found on this CRM server.</p>
        <p><a href="/crm/">Back to CRM Home</a></p>
    </body>
    </html>
    """), 404

if __name__ == '__main__':
    # Ensure log directory exists
    import os
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                Lingdang CRM SQL Injection Honeypot          ║
║                        CVE-2025-9140                         ║
╠══════════════════════════════════════════════════════════════╣
║ Listening on: {config.HOST}:{config.PORT}                                ║
║ Vulnerable endpoint: /crm/crmapi/erp/tabdetail_moduleSave.php║
║ Log file: {config.LOG_FILE}                              ║
║ Simulation mode: {'ON' if config.SIMULATE_VULNERABLE else 'OFF'}                                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    logger.info("Honeypot started")
    
    # Run the Flask application
    try:
        run_simple(config.HOST, config.PORT, app, use_reloader=False, use_debugger=config.DEBUG)
    except KeyboardInterrupt:
        logger.info("Honeypot stopped by user")
        print("\nHoneypot stopped.")