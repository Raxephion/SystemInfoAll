# System Information Tool

A Python script that extracts comprehensive hardware and system information from any system, similar to `lshw`, `uname`, and `hostnamectl` on Linux.

## Features

- **System Info**: OS, hostname, release, version, architecture
- **CPU Details**: Cores, frequencies, usage per core
- **Memory Stats**: RAM and swap usage with percentages
- **Disk Info**: Partitions, usage, I/O statistics
- **Network Data**: Interfaces, IP addresses, MAC addresses, traffic stats
- **Boot Time**: System startup timestamp
- **File Export**: Saves all information to `sysinfo.txt`

## Requirements

```bash
pip install psutil
Usage
bashpython system_info.py

```
Output is displayed in terminal and saved to ~/sysinfo.txt
Use Cases

Use Cases

IT Support: Quick system diagnostics and hardware inventory
System Monitoring: Performance baseline establishment
Asset Management: Hardware audit and documentation
Troubleshooting: Resource usage analysis for performance issues
Security Audits: Network interface and system configuration review
Documentation: Automated system specification reports
DevOps: Infrastructure inventory and monitoring
Remote Support: Gather system info from client machines
Compliance: Hardware/software inventory for regulatory requirements
Testing: Environment documentation for QA and development

Cross-Platform
Works on Windows, Linux, and macOS.
