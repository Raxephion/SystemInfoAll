# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 11:42:00 2022

@author: Pierre-Henri Rossouw

Application for extracting all hardware and system information on any system
similar to Ishw, uname and hostnamectl on Linux

"""
#importing modules 

import psutil
import platform
from datetime import datetime


# Define function that converts large numbers of bytes into a scaled format

def get_size(bytes, suffix = "B"):
    """
    This function converts large numbers of bytes into a scaled format
    
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
        
#Basic system information
       
print("="*40, "System Information", "="*40)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"Node Name: {uname.node}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor: {uname.processor}")


#Boot time information
    
print("="*40, "Boot Time", "="*40)
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
print(f"Boot Time: {bt.year}/{bt.month}/{bt.day}  {bt.hour}:{bt.minute}:{bt.second}")


#CPU Information

print("-"*40, "CPU Info", "-"*40)
#Number of Cores
print("Physical Cores:", psutil.cpu_count(logical=False))
print("Total Cores:", psutil.cpu_count(logical = True))
#CPU Frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max: .2f}Mhz")
print(f"Min Frequency: {cpufreq.min: .2f}Mhz")
print(f"Current Frequency: {cpufreq.current: .2f}Mhz")
#CPU Usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")


#Memory Usage

#Memory Information
print("-"*40, "Memory Information", "-"*40)
#Get Memory Details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("="*20, "SWAP", "="*20)
#Get the swap memory details (if available)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"FRee: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")


#Disk Usage

#Disk Information
print("-"*40, "Disk Information", "-"*40)
print("Partitions and Usage: ")
#Get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"   Mountpoint: {partition.mountpoint}")
    print(f"   File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        #This can be catcheddue to the disk that is not ready
        continue
    print(f" Total Size: {get_size(partition_usage.total)}")
    print(f" Used: {get_size(partition_usage.used)}")
    print(f" Free: {get_size(partition_usage.free)}")
    print(f" Percentage: {partition_usage.percent}%")
#Get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total write: {get_size(disk_io.write_bytes)}")


#Network Information

print("-"*40, "Network Information", "-"*40)
#Get all network interfaces (Virtual and Physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f" IP Address: {address.address}")
            print(f" Netmask: {address.netmask}")
            print(f" Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f" MAC address: {address.address}")
            print(f" Broadcast MAC: {address.broadcast}")
#Get IO Statistics since boot
net_io = psutil.net_io_counters()
print(f" Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f" Total Bytes Received: {get_size(net_io.bytes_recv)}")


#Now to write all the above information to file and save it
#with open ("c:\\Users\\user\\sysinfo.txt", "w") as f:
#    f.write("="*40, "System Information", "="*40)
#    f.write(f"System: {uname.system}")
#    f.write(f"Node Name: {uname.node}")
    
xfile = open("c:\\Users\\user\\sysinfo.txt", "w")
xfile.write(f" MAC address: {address.address}")
xfile.write(f" Netmask: {address.netmask}")
xfile.write(f" IP Address: {address.address}")






