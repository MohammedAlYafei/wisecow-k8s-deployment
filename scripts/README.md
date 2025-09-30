# DevOps Monitoring Scripts

Collection of system and application monitoring scripts for DevOps automation.

## 📋 Scripts Included

### 1. System Health Monitor (`system_health_monitor.sh`)

Bash script that monitors Linux/Unix system health metrics.

**Features:**
- CPU usage monitoring
- Memory utilization check
- Disk space monitoring
- Running processes overview
- System uptime
- Configurable thresholds
- Colored console output
- Automatic logging

**Usage:**
```bash
# Run health check
./system_health_monitor.sh

# Output saved to: logs/system_health_YYYYMMDD.log

    Configuration:
Edit thresholds in script:

CPU_THRESHOLD=80 (%)
MEMORY_THRESHOLD=80 (%)
DISK_THRESHOLD=80 (%)


    Example Output :-

================================
  SYSTEM HEALTH MONITORING
  2025-09-30 17:50:00
================================

[CPU CHECK]
CPU Usage: 45%
✓ CPU usage is normal

[MEMORY CHECK]
Memory Usage: 62% (Used: 5.2G / Total: 8.0G)
✓ Memory usage is normal

[DISK CHECK]
Disk Usage: 55% on /dev/sda1 (/)
✓ Disk usage is normal
 

2. Application Health Checker (app_health_checker.py)
Python script that monitors application uptime via HTTP status codes.
Features:

Multi-application monitoring
HTTP status code checking
Response time measurement
Connection error handling
Detailed logging
Summary reports
Colored output
Continuous monitoring mode

Prerequisites:
bashpip install requests
Usage:
Single Check:
bashpython app_health_checker.py
Continuous Monitoring:
bash# Check every 30 seconds
python app_health_checker.py --interval 30

# Stop with Ctrl+C
Custom Configuration:
bash# Use custom config file
python app_health_checker.py --config apps.json
Configuration File Format (apps.json):
json[
  {
    "name": "My App",
    "url": "https://myapp.com",
    "expected_status": 200,
    "timeout": 5
  },
  {
    "name": "API Service",
    "url": "https://api.myapp.com/health",
    "expected_status": 200,
    "timeout": 10
  }
]
Example Output:
==================================================
  APPLICATION HEALTH CHECKER
  2025-09-30 17:54:25
==================================================

[✓] Google
    URL: https://www.google.com
    Status Code: 200
    Response Time: 1296.95ms

[✗] Invalid Site (Demo)
    URL: https://thissitedoesnotexist12345.com
    Error: Connection failed

==================================================
SUMMARY REPORT
==================================================
Total Applications: 3
UP: 2
DOWN: 1
Log File: logs/app_health_20250930.log
==================================================
Status Indicators:

✓ UP - Application is running (2xx status)
✗ DOWN - Application is unreachable
⚠ CLIENT_ERROR - 4xx status codes
⚠ SERVER_ERROR - 5xx status codes


📁 Directory Structure
scripts/
├── README.md
├── system_health_monitor.sh
├── app_health_checker.py
└── logs/
    ├── system_health_20250930.log
    └── app_health_20250930.log

🚀 Quick Start
bash# Make scripts executable
chmod +x system_health_monitor.sh
chmod +x app_health_checker.py

# Install Python dependencies
pip install requests

# Run system health check
./system_health_monitor.sh

# Run application health check
python app_health_checker.py

📊 Automation
