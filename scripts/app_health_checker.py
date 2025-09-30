#!/usr/bin/env python3

"""
Application Health Checker Script
Monitors application uptime and health via HTTP status codes
Author: Your Name
Date: 2024
"""

import requests
import time
import json
from datetime import datetime
from typing import Dict, List
import sys

# Color codes for terminal output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class AppHealthChecker:
    def __init__(self, config_file: str = None):
        """Initialize the health checker with configuration"""
        self.log_file = f"logs/app_health_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Default applications to monitor
        self.applications = [
            {
                "name": "Google",
                "url": "https://www.google.com",
                "expected_status": 200,
                "timeout": 5
            },
            {
                "name": "GitHub",
                "url": "https://github.com",
                "expected_status": 200,
                "timeout": 5
            },
            {
                "name": "Invalid Site (Demo)",
                "url": "https://thissitedoesnotexist12345.com",
                "expected_status": 200,
                "timeout": 5
            }
        ]
        
        # Load custom config if provided
        if config_file:
            self.load_config(config_file)
    
    def load_config(self, config_file: str):
        """Load application configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                self.applications = json.load(f)
            self.log_message(f"Loaded configuration from {config_file}")
        except Exception as e:
            self.log_message(f"ERROR: Failed to load config: {str(e)}", level="ERROR")
    
    def log_message(self, message: str, level: str = "INFO"):
        """Log messages to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Write to log file
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry + '\n')
        except Exception as e:
            print(f"Failed to write to log: {str(e)}")
    
    def print_header(self):
        """Print script header"""
        print(f"\n{Colors.GREEN}{'='*50}{Colors.NC}")
        print(f"{Colors.GREEN}  APPLICATION HEALTH CHECKER{Colors.NC}")
        print(f"{Colors.GREEN}  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.NC}")
        print(f"{Colors.GREEN}{'='*50}{Colors.NC}\n")
    
    def check_application(self, app: Dict) -> Dict:
        """Check health of a single application"""
        name = app.get('name', 'Unknown')
        url = app.get('url', '')
        expected_status = app.get('expected_status', 200)
        timeout = app.get('timeout', 5)
        
        result = {
            'name': name,
            'url': url,
            'status': 'UNKNOWN',
            'status_code': None,
            'response_time': None,
            'error': None
        }
        
        try:
            # Make HTTP request
            start_time = time.time()
            response = requests.get(url, timeout=timeout, allow_redirects=True)
            response_time = round((time.time() - start_time) * 1000, 2)  # in ms
            
            result['status_code'] = response.status_code
            result['response_time'] = response_time
            
            # Determine status
            if response.status_code == expected_status:
                result['status'] = 'UP'
            elif 200 <= response.status_code < 300:
                result['status'] = 'UP'
            elif 300 <= response.status_code < 400:
                result['status'] = 'REDIRECT'
            elif 400 <= response.status_code < 500:
                result['status'] = 'CLIENT_ERROR'
            elif 500 <= response.status_code < 600:
                result['status'] = 'SERVER_ERROR'
            else:
                result['status'] = 'UNKNOWN'
                
        except requests.exceptions.Timeout:
            result['status'] = 'DOWN'
            result['error'] = 'Request timeout'
        except requests.exceptions.ConnectionError:
            result['status'] = 'DOWN'
            result['error'] = 'Connection failed'
        except requests.exceptions.RequestException as e:
            result['status'] = 'DOWN'
            result['error'] = str(e)
        except Exception as e:
            result['status'] = 'ERROR'
            result['error'] = str(e)
        
        return result
    
    def print_result(self, result: Dict):
        """Print health check result with colors"""
        status = result['status']
        name = result['name']
        url = result['url']
        status_code = result['status_code']
        response_time = result['response_time']
        error = result['error']
        
        # Status color
        if status == 'UP':
            status_color = Colors.GREEN
            status_icon = '✓'
        elif status in ['DOWN', 'SERVER_ERROR']:
            status_color = Colors.RED
            status_icon = '✗'
        elif status in ['CLIENT_ERROR', 'REDIRECT']:
            status_color = Colors.YELLOW
            status_icon = '⚠'
        else:
            status_color = Colors.BLUE
            status_icon = '?'
        
        print(f"{status_color}[{status_icon}] {name}{Colors.NC}")
        print(f"    URL: {url}")
        
        if status_code:
            print(f"    Status Code: {status_code}")
        if response_time:
            print(f"    Response Time: {response_time}ms")
        if error:
            print(f"    Error: {error}")
        
        print()
        
        # Log result
        log_msg = f"{name} ({url}) - Status: {status}"
        if status_code:
            log_msg += f" | Code: {status_code}"
        if response_time:
            log_msg += f" | Time: {response_time}ms"
        if error:
            log_msg += f" | Error: {error}"
        
        level = "ERROR" if status == 'DOWN' else "INFO"
        self.log_message(log_msg, level=level)
    
    def generate_summary(self, results: List[Dict]):
        """Generate and print summary report"""
        total = len(results)
        up = sum(1 for r in results if r['status'] == 'UP')
        down = sum(1 for r in results if r['status'] == 'DOWN')
        errors = sum(1 for r in results if r['status'] in ['CLIENT_ERROR', 'SERVER_ERROR', 'ERROR'])
        
        print(f"{Colors.BLUE}{'='*50}{Colors.NC}")
        print(f"{Colors.BLUE}SUMMARY REPORT{Colors.NC}")
        print(f"{Colors.BLUE}{'='*50}{Colors.NC}")
        print(f"Total Applications: {total}")
        print(f"{Colors.GREEN}UP: {up}{Colors.NC}")
        print(f"{Colors.RED}DOWN: {down}{Colors.NC}")
        print(f"{Colors.YELLOW}ERRORS: {errors}{Colors.NC}")
        print(f"Log File: {self.log_file}")
        print(f"{Colors.BLUE}{'='*50}{Colors.NC}\n")
        
        self.log_message(f"Summary - Total: {total}, UP: {up}, DOWN: {down}, ERRORS: {errors}")
    
    def run(self, interval: int = None):
        """Run health checks (once or continuously)"""
        self.print_header()
        
        if interval:
            print(f"Running in continuous mode (interval: {interval}s)")
            print(f"Press Ctrl+C to stop\n")
            try:
                while True:
                    results = []
                    for app in self.applications:
                        result = self.check_application(app)
                        self.print_result(result)
                        results.append(result)
                    
                    self.generate_summary(results)
                    time.sleep(interval)
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Health checker stopped by user{Colors.NC}")
                sys.exit(0)
        else:
            # Single run
            results = []
            for app in self.applications:
                result = self.check_application(app)
                self.print_result(result)
                results.append(result)
            
            self.generate_summary(results)


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Application Health Checker')
    parser.add_argument('-c', '--config', help='Configuration file (JSON)', default=None)
    parser.add_argument('-i', '--interval', type=int, help='Check interval in seconds (continuous mode)', default=None)
    
    args = parser.parse_args()
    
    # Create checker instance
    checker = AppHealthChecker(config_file=args.config)
    
    # Run checks
    checker.run(interval=args.interval)


if __name__ == "__main__":
    main()
