# Configuration for Lingdang CRM SQL Injection Honeypot

# Server settings
HOST = '0.0.0.0'
PORT = 8080
DEBUG = False

# Logging settings
LOG_FILE = 'logs/honeypot.log'
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Attack simulation settings
SIMULATE_DELAY = True  # Whether to simulate time delays for time-based SQLi
DEFAULT_DELAY = 5.0    # Default delay in seconds for SLEEP() payloads
MAX_DELAY = 10.0       # Maximum delay to prevent DoS

# Response settings
SIMULATE_VULNERABLE = True  # Whether to act vulnerable or return errors
FAKE_ERROR_RESPONSES = [
    "MySQL error: You have an error in your SQL syntax",
    "Warning: mysql_fetch_array() expects parameter",
    "Database connection failed",
    "Internal server error occurred"
]

# Detection patterns for common SQL injection payloads
SQLI_PATTERNS = [
    # Time-based patterns
    r"sleep\s*\(\s*\d+\s*\)",
    r"waitfor\s+delay",
    r"pg_sleep\s*\(",
    r"benchmark\s*\(",
    
    # Boolean-based patterns
    r"'\s*(or|and)\s+\d+\s*=\s*\d+",
    r"union\s+select",
    r"'.*--",
    r"'.*#",
    
    # Error-based patterns
    r"extractvalue\s*\(",
    r"updatexml\s*\(",
    r"exp\s*\(\s*~",
    
    # Generic SQL keywords
    r"(select|insert|update|delete|drop|create|alter|exec|execute)\s+",
    r"information_schema",
    r"sysdatabases",
    r"pg_database"
]

# Geolocation and threat intelligence (optional)
ENABLE_GEOLOCATION = False
GEOIP_DATABASE_PATH = None

# Alert settings
ENABLE_ALERTS = True
ALERT_THRESHOLD = 5  # Number of attacks before sending alert
ALERT_EMAIL = None   # Email address for alerts (if configured)