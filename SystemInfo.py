# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 11:42:00 2022

@author: Pierre-Henri Rossouw

Application for extracting all hardware and system information on any system
similar to lshw, uname and hostnamectl on Linux

"""
# Importing modules 
import psutil
import platform
from datetime import datetime
import os


# Define function that converts large numbers of bytes into a scaled format
def get_size(bytes, suffix="B"):
    """
    This function converts large numbers of bytes into a scaled format
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# Function to write system info to file
def write_system_info_to_file():
    """
    Write all system information to a file
    """
    # Use a more portable path approach
    output_file = os.path.join(os.path.expanduser("~"), "sysinfo.txt")
    
    try:
        with open(output_file, "w") as f:
            # Basic system information
            f.write("=" * 40 + " System Information " + "=" * 40 + "\n")
            uname = platform.uname()
            f.write(f"System: {uname.system}\n")
            f.write(f"Node Name: {uname.node}\n")
            f.write(f"Release: {uname.release}\n")
            f.write(f"Version: {uname.version}\n")
            f.write(f"Machine: {uname.machine}\n")
            f.write(f"Processor: {uname.processor}\n\n")
            
            # Boot time information
            f.write("=" * 40 + " Boot Time " + "=" * 40 + "\n")
            boot_time_timestamp = psutil.boot_time()
            bt = datetime.fromtimestamp(boot_time_timestamp)
            f.write(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n\n")
            
            # CPU Information
            f.write("-" * 40 + " CPU Info " + "-" * 40 + "\n")
            f.write(f"Physical Cores: {psutil.cpu_count(logical=False)}\n")
            f.write(f"Total Cores: {psutil.cpu_count(logical=True)}\n")
            
            # CPU Frequencies (handle case where it might not be available)
            try:
                cpufreq = psutil.cpu_freq()
                if cpufreq:
                    f.write(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
                    f.write(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
                    f.write(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
                else:
                    f.write("CPU frequency information not available\n")
            except Exception as e:
                f.write(f"CPU frequency information not available: {e}\n")
            
            # CPU Usage
            f.write("CPU Usage Per Core:\n")
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                f.write(f"Core {i}: {percentage}%\n")
            f.write(f"Total CPU Usage: {psutil.cpu_percent()}%\n\n")
            
            # Memory Information
            f.write("-" * 40 + " Memory Information " + "-" * 40 + "\n")
            svmem = psutil.virtual_memory()
            f.write(f"Total: {get_size(svmem.total)}\n")
            f.write(f"Available: {get_size(svmem.available)}\n")
            f.write(f"Used: {get_size(svmem.used)}\n")
            f.write(f"Percentage: {svmem.percent}%\n")
            f.write("=" * 20 + " SWAP " + "=" * 20 + "\n")
            
            # Get the swap memory details (if available)
            swap = psutil.swap_memory()
            f.write(f"Total: {get_size(swap.total)}\n")
            f.write(f"Free: {get_size(swap.free)}\n")
            f.write(f"Used: {get_size(swap.used)}\n")
            f.write(f"Percentage: {swap.percent}%\n\n")
            
            # Disk Information
            f.write("-" * 40 + " Disk Information " + "-" * 40 + "\n")
            f.write("Partitions and Usage:\n")
            partitions = psutil.disk_partitions()
            for partition in partitions:
                f.write(f"=== Device: {partition.device} ===\n")
                f.write(f"   Mountpoint: {partition.mountpoint}\n")
                f.write(f"   File system type: {partition.fstype}\n")
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                    f.write(f"   Total Size: {get_size(partition_usage.total)}\n")
                    f.write(f"   Used: {get_size(partition_usage.used)}\n")
                    f.write(f"   Free: {get_size(partition_usage.free)}\n")
                    f.write(f"   Percentage: {partition_usage.percent}%\n")
                except PermissionError:
                    f.write("   Permission denied to access this partition\n")
                except Exception as e:
                    f.write(f"   Error accessing partition: {e}\n")
            
            # Get IO statistics since boot
            try:
                disk_io = psutil.disk_io_counters()
                if disk_io:
                    f.write(f"Total read: {get_size(disk_io.read_bytes)}\n")
                    f.write(f"Total write: {get_size(disk_io.write_bytes)}\n\n")
                else:
                    f.write("Disk I/O statistics not available\n\n")
            except Exception as e:
                f.write(f"Disk I/O statistics not available: {e}\n\n")
            
            # Network Information
            f.write("-" * 40 + " Network Information " + "-" * 40 + "\n")
            if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addresses in if_addrs.items():
                f.write(f"=== Interface: {interface_name} ===\n")
                for address in interface_addresses:
                    if str(address.family) == 'AddressFamily.AF_INET':
                        f.write(f"   IP Address: {address.address}\n")
                        f.write(f"   Netmask: {address.netmask}\n")
                        f.write(f"   Broadcast IP: {address.broadcast}\n")
                    elif str(address.family) == 'AddressFamily.AF_PACKET':
                        f.write(f"   MAC Address: {address.address}\n")
                        f.write(f"   Broadcast MAC: {address.broadcast}\n")
            
            # Get IO Statistics since boot
            try:
                net_io = psutil.net_io_counters()
                if net_io:
                    f.write(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n")
                    f.write(f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n")
                else:
                    f.write("Network I/O statistics not available\n")
            except Exception as e:
                f.write(f"Network I/O statistics not available: {e}\n")
                
        print(f"System information successfully written to: {output_file}")
        
    except Exception as e:
        print(f"Error writing to file: {e}")


# Main execution
if __name__ == "__main__":
    # Basic system information
    print("=" * 40, "System Information", "=" * 40)
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")

    # Boot time information
    print("=" * 40, "Boot Time", "=" * 40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

    # CPU Information
    print("-" * 40, "CPU Info", "-" * 40)
    # Number of Cores
    print("Physical Cores:", psutil.cpu_count(logical=False))
    print("Total Cores:", psutil.cpu_count(logical=True))
    
    # CPU Frequencies (handle case where it might not be available)
    try:
        cpufreq = psutil.cpu_freq()
        if cpufreq:
            print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
            print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
            print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
        else:
            print("CPU frequency information not available")
    except Exception as e:
        print(f"CPU frequency information not available: {e}")
    
    # CPU Usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")

    # Memory Information
    print("-" * 40, "Memory Information", "-" * 40)
    # Get Memory Details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("=" * 20, "SWAP", "=" * 20)
    # Get the swap memory details (if available)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")

    # Disk Information
    print("-" * 40, "Disk Information", "-" * 40)
    print("Partitions and Usage:")
    # Get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"   Mountpoint: {partition.mountpoint}")
        print(f"   File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            print(f"   Total Size: {get_size(partition_usage.total)}")
            print(f"   Used: {get_size(partition_usage.used)}")
            print(f"   Free: {get_size(partition_usage.free)}")
            print(f"   Percentage: {partition_usage.percent}%")
        except PermissionError:
            # This can be caught due to the disk that is not ready
            print("   Permission denied to access this partition")
            continue
        except Exception as e:
            print(f"   Error accessing partition: {e}")
            continue
    
    # Get IO statistics since boot
    try:
        disk_io = psutil.disk_io_counters()
        if disk_io:
            print(f"Total read: {get_size(disk_io.read_bytes)}")
            print(f"Total write: {get_size(disk_io.write_bytes)}")
        else:
            print("Disk I/O statistics not available")
    except Exception as e:
        print(f"Disk I/O statistics not available: {e}")

    # Network Information
    print("-" * 40, "Network Information", "-" * 40)
    # Get all network interfaces (Virtual and Physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        print(f"=== Interface: {interface_name} ===")
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"   IP Address: {address.address}")
                print(f"   Netmask: {address.netmask}")
                print(f"   Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"   MAC Address: {address.address}")
                print(f"   Broadcast MAC: {address.broadcast}")
    
    # Get IO Statistics since boot
    try:
        net_io = psutil.net_io_counters()
        if net_io:
            print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
            print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
        else:
            print("Network I/O statistics not available")
    except Exception as e:
        print(f"Network I/O statistics not available: {e}")

    # Write all information to file
    write_system_info_to_file()
