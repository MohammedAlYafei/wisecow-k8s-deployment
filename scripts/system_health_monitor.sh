#!/bin/bash

############################################
# System Health Monitoring Script
# Monitors: CPU, Memory, Disk, Processes
# Author: Your Name
# Date: $(date +%Y-%m-%d)
############################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Thresholds (customize as needed)
CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
DISK_THRESHOLD=80

# Log file
LOG_FILE="logs/system_health_$(date +%Y%m%d).log"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to print header
print_header() {
    echo -e "\n${GREEN}================================${NC}"
    echo -e "${GREEN}  SYSTEM HEALTH MONITORING${NC}"
    echo -e "${GREEN}  $(date '+%Y-%m-%d %H:%M:%S')${NC}"
    echo -e "${GREEN}================================${NC}\n"
}

# Function to check CPU usage
check_cpu() {
    echo -e "${YELLOW}[CPU CHECK]${NC}"
    
    # Get CPU usage (works on Linux and macOS)
    if command -v top &> /dev/null; then
        if [[ "$OSTYPE" == "linux-gnu"* ]]; then
            CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
        elif [[ "$OSTYPE" == "darwin"* ]]; then
            CPU_USAGE=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | cut -d'%' -f1)
        else
            CPU_USAGE=$(wmic cpu get loadpercentage | grep -v LoadPercentage | tr -d ' ')
        fi
    else
        CPU_USAGE=0
    fi
    
    CPU_USAGE=${CPU_USAGE:-0}
    
    echo "CPU Usage: ${CPU_USAGE}%"
    
    if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l 2>/dev/null || echo 0) )); then
        echo -e "${RED}⚠ ALERT: CPU usage is above ${CPU_THRESHOLD}%${NC}"
        log_message "ALERT: CPU usage is ${CPU_USAGE}% (Threshold: ${CPU_THRESHOLD}%)"
    else
        echo -e "${GREEN}✓ CPU usage is normal${NC}"
        log_message "INFO: CPU usage is ${CPU_USAGE}%"
    fi
    echo ""
}

# Function to check Memory usage
check_memory() {
    echo -e "${YELLOW}[MEMORY CHECK]${NC}"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
        TOTAL_MEM=$(free -h | grep Mem | awk '{print $2}')
        USED_MEM=$(free -h | grep Mem | awk '{print $3}')
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        MEMORY_USAGE=$(vm_stat | awk '/Pages active/ {active=$3} /Pages wired/ {wired=$4} /Pages free/ {free=$3} END {printf "%.0f", (active+wired)/(active+wired+free)*100}')
        TOTAL_MEM=$(sysctl hw.memsize | awk '{printf "%.1fG", $2/1024/1024/1024}')
        USED_MEM="N/A"
    else
        MEMORY_USAGE=0
        TOTAL_MEM="N/A"
        USED_MEM="N/A"
    fi
    
    echo "Memory Usage: ${MEMORY_USAGE}% (Used: ${USED_MEM} / Total: ${TOTAL_MEM})"
    
    if [ "$MEMORY_USAGE" -gt "$MEMORY_THRESHOLD" ]; then
        echo -e "${RED}⚠ ALERT: Memory usage is above ${MEMORY_THRESHOLD}%${NC}"
        log_message "ALERT: Memory usage is ${MEMORY_USAGE}% (Threshold: ${MEMORY_THRESHOLD}%)"
    else
        echo -e "${GREEN}✓ Memory usage is normal${NC}"
        log_message "INFO: Memory usage is ${MEMORY_USAGE}%"
    fi
    echo ""
}

# Function to check Disk usage
check_disk() {
    echo -e "${YELLOW}[DISK CHECK]${NC}"
    
    df -h | grep -vE '^Filesystem|tmpfs|cdrom|loop' | awk '{print $5 " " $1 " " $6}' | while read output;
    do
        usage=$(echo $output | awk '{print $1}' | sed 's/%//g')
        partition=$(echo $output | awk '{print $2}')
        mount=$(echo $output | awk '{print $3}')
        
        echo "Disk Usage: ${usage}% on ${partition} (${mount})"
        
        if [ "$usage" -gt "$DISK_THRESHOLD" ]; then
            echo -e "${RED}⚠ ALERT: Disk usage is above ${DISK_THRESHOLD}% on ${partition}${NC}"
            log_message "ALERT: Disk usage is ${usage}% on ${partition} (Threshold: ${DISK_THRESHOLD}%)"
        else
            echo -e "${GREEN}✓ Disk usage is normal on ${partition}${NC}"
        fi
    done
    echo ""
}

# Function to check running processes
check_processes() {
    echo -e "${YELLOW}[PROCESS CHECK]${NC}"
    
    PROCESS_COUNT=$(ps aux | wc -l)
    echo "Total Running Processes: ${PROCESS_COUNT}"
    
    echo -e "\nTop 5 CPU consuming processes:"
    ps aux --sort=-%cpu | head -6 | tail -5 | awk '{printf "  %-10s %-6s %-6s %s\n", $1, $2, $3, $11}'
    
    echo -e "\nTop 5 Memory consuming processes:"
    ps aux --sort=-%mem | head -6 | tail -5 | awk '{printf "  %-10s %-6s %-6s %s\n", $1, $2, $4, $11}'
    
    log_message "INFO: Total running processes: ${PROCESS_COUNT}"
    echo ""
}

# Function to check system uptime
check_uptime() {
    echo -e "${YELLOW}[SYSTEM UPTIME]${NC}"
    uptime
    log_message "INFO: System uptime - $(uptime)"
    echo ""
}

# Main execution
main() {
    print_header
    check_cpu
    check_memory
    check_disk
    check_processes
    check_uptime
    
    echo -e "${GREEN}================================${NC}"
    echo -e "${GREEN}Health check completed!${NC}"
    echo -e "${GREEN}Log saved to: $LOG_FILE${NC}"
    echo -e "${GREEN}================================${NC}\n"
}

# Run main function
main
