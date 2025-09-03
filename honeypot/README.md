# Lingdang CRM 8.6.4.7 SQL Injection Honeypot

A honeypot implementation that simulates the vulnerable Lingdang CRM endpoint affected by **CVE-2025-9140**, designed for threat intelligence gathering and security research.

## Overview

This honeypot simulates the SQL injection vulnerability found in Lingdang CRM version 8.6.4.7 and earlier. The vulnerability exists in the `/crm/crmapi/erp/tabdetail_moduleSave.php` endpoint via the `getvaluestring` parameter, allowing both time-based and boolean-based blind SQL injection attacks.

### Vulnerability Details

- **CVE ID**: CVE-2025-9140
- **VulDB ID**: VDB-320520
- **Affected Version**: Lingdang CRM ≤ 8.6.4.7
- **Vulnerability Type**: SQL Injection (CWE-89)
- **Attack Vector**: Remote, Unauthenticated
- **Vulnerable Parameter**: `getvaluestring` (GET/POST)
- **Vulnerable Endpoint**: `/crm/crmapi/erp/tabdetail_moduleSave.php`

## Features

### 🎯 Attack Detection
- **Time-based SQL Injection**: Detects and simulates delays for `SLEEP()`, `WAITFOR DELAY`, `pg_sleep()`, and `BENCHMARK()` payloads
- **Boolean-based SQL Injection**: Responds differently to true/false conditions
- **Error-based SQL Injection**: Returns realistic database error messages
- **Pattern Recognition**: Comprehensive regex patterns for SQL injection detection

### 📊 Logging & Intelligence
- Detailed attack logging with IP addresses, user agents, and payloads
- JSON-structured logs for easy parsing and analysis
- Attack frequency tracking per IP address
- Configurable alert thresholds

### 🎭 Realistic Simulation
- Mimics actual CRM interface with login pages and directory structure
- Configurable response delays and error messages
- Authentic-looking HTML responses
- Statistics endpoint for monitoring

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

1. **Clone and navigate to the honeypot directory:**
   ```bash
   git clone <repository-url>
   cd larsjelle.github.io/honeypot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the honeypot (optional):**
   Edit `config.py` to customize settings:
   ```python
   # Server settings
   HOST = '0.0.0.0'  # Listen on all interfaces
   PORT = 8080       # Change port if needed
   
   # Enable/disable attack simulation
   SIMULATE_VULNERABLE = True
   SIMULATE_DELAY = True
   DEFAULT_DELAY = 5.0
   ```

4. **Run the honeypot:**
   ```bash
   python3 lingdang_crm_honeypot.py
   ```

## Usage

### Testing the Honeypot

The honeypot will be available at `http://your-server:8080/crm/`

**Test with the original exploit payloads:**

```bash
# Time-based SQL injection (should cause ~5 second delay)
curl -i "http://localhost:8080/crm/crmapi/erp/tabdetail_moduleSave.php?getvaluestring='||(SELECT SLEEP(5))--+-"

# Boolean-based SQL injection (true condition)
curl -i "http://localhost:8080/crm/crmapi/erp/tabdetail_moduleSave.php?getvaluestring=' OR 1=1-- -"

# Boolean-based SQL injection (false condition)
curl -i "http://localhost:8080/crm/crmapi/erp/tabdetail_moduleSave.php?getvaluestring=' OR 1=2-- -"

# POST method attack
curl -i -X POST "http://localhost:8080/crm/crmapi/erp/tabdetail_moduleSave.php" \
     --data "getvaluestring='||(SELECT SLEEP(5))--+-"
```

### Monitoring

**View statistics:**
```bash
curl http://localhost:8080/stats
```

**Monitor logs in real-time:**
```bash
tail -f logs/honeypot.log
```

## Configuration Options

### Core Settings
- `HOST`: Server bind address (default: '0.0.0.0')
- `PORT`: Server port (default: 8080)
- `DEBUG`: Flask debug mode (default: False)

### Attack Simulation
- `SIMULATE_VULNERABLE`: Enable vulnerable behavior (default: True)
- `SIMULATE_DELAY`: Enable time delays for time-based attacks (default: True)
- `DEFAULT_DELAY`: Default sleep time in seconds (default: 5.0)
- `MAX_DELAY`: Maximum allowed delay to prevent DoS (default: 10.0)

### Detection Patterns
The honeypot includes comprehensive SQL injection patterns:
- Time-based: `SLEEP()`, `WAITFOR DELAY`, `pg_sleep()`, `BENCHMARK()`
- Boolean-based: `OR 1=1`, `AND 1=2`, `UNION SELECT`
- Error-based: `extractvalue()`, `updatexml()`, `exp()`
- Generic SQL keywords and injection indicators

### Alerting
- `ENABLE_ALERTS`: Enable critical alerts (default: True)
- `ALERT_THRESHOLD`: Number of attacks before alerting (default: 5)
- `ALERT_EMAIL`: Email for notifications (optional)

## Log Format

Attacks are logged in JSON format:

```json
{
  "timestamp": "2025-01-01T12:00:00.000000",
  "ip_address": "192.168.1.100",
  "user_agent": "curl/7.68.0",
  "method": "GET",
  "url": "http://localhost:8080/crm/crmapi/erp/tabdetail_moduleSave.php?getvaluestring='||(SELECT SLEEP(5))--+-",
  "parameters": {"getvaluestring": "'||(SELECT SLEEP(5))--+-"},
  "is_attack": true,
  "matched_patterns": ["sleep\\s*\\(\\s*\\d+\\s*\\)"],
  "delay_applied": 5.0,
  "headers": {"Host": "localhost:8080", "User-Agent": "curl/7.68.0"}
}
```

## Security Considerations

⚠️ **Important Security Notes:**

1. **Isolated Environment**: Deploy in a sandboxed/isolated environment
2. **Network Segmentation**: Isolate from production networks
3. **Monitoring**: Continuously monitor honeypot activity
4. **Resource Limits**: Configure appropriate resource limits to prevent DoS
5. **Legal Compliance**: Ensure deployment complies with local laws and regulations

## Advanced Usage

### Custom Response Simulation

Modify `generate_vulnerable_response()` to simulate specific application behavior:

```python
def generate_vulnerable_response(payload, is_attack, patterns, delay_applied):
    if is_attack and 'union' in payload.lower():
        # Simulate data extraction response
        return jsonify({
            'users': ['admin', 'user1', 'guest'],
            'version': '8.6.4.7'
        })
```

### Integration with SIEM

Parse logs and forward to SIEM systems:

```bash
# Parse and forward to syslog
tail -f logs/honeypot.log | while read line; do
    logger -p local0.info "HONEYPOT: $line"
done
```

## Troubleshooting

### Common Issues

1. **Port binding error**: Change `PORT` in config.py or run as administrator
2. **Import errors**: Install requirements with `pip install -r requirements.txt`
3. **Permission errors**: Ensure write permissions for logs directory
4. **No attacks detected**: Verify patterns in `config.py` are correct

### Debug Mode

Enable debug mode for troubleshooting:
```python
DEBUG = True  # in config.py
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request

## Disclaimer

This honeypot is intended for:
- ✅ Security research and education
- ✅ Threat intelligence gathering
- ✅ Testing detection capabilities
- ✅ Understanding attack patterns

**NOT intended for:**
- ❌ Attacking real systems
- ❌ Illegal activities
- ❌ Unauthorized testing

## License

This project is provided for educational and research purposes. Use responsibly and in compliance with applicable laws and regulations.

## References

- [CVE-2025-9140](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2025-9140)
- [Original Exploit (ExploitDB #52420)](https://www.exploit-db.com/exploits/52420)
- [VulDB Entry VDB-320520](https://vuldb.com/?id.320520)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)

---

**⚡ Happy Threat Hunting!**