import subprocess
import json

def get_list_of_pods():
    """
    Get list of pods in the current namespace using kubectl get pod command.
    
    Returns:
        list: A list of pod names in the current namespace
    """
    try:
        # Execute kubectl command to get pods in JSON format
        result = subprocess.run(
            ["kubectl", "get", "pods", "-o", "json"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the JSON output
        pods_data = json.loads(result.stdout)
        
        # Extract pod names from the items list
        pod_names = [item["metadata"]["name"] for item in pods_data["items"] 
                    if item["status"]["phase"] == "Running"]
        
        return pod_names
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing kubectl command: {e}")
        print(f"Error output: {e.stderr}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing kubectl output: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def get_download_usage_per_pod():
    """
    Get download network usage for each pod.
    
    Returns:
        dict: A dictionary mapping pod names to their download usage in bytes
    """
    download_usage = {}
    pods = get_list_of_pods()
    
    for pod in pods:
        try:
            # Execute kubectl exec to read network interface statistics
            result = subprocess.run(
                ["kubectl", "exec", pod, "--", "cat", "/proc/net/dev"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output of /proc/net/dev
            # The format is: Interface: Receive bytes packets errs drop fifo frame compressed multicast Transmit bytes ...
            lines = result.stdout.strip().split('\n')
            
            # Skip the header lines (first two lines)
            data_lines = lines[2:]
            
            total_bytes_received = 0
            
            for line in data_lines:
                # Split by colon to separate interface name from stats
                if ':' in line:
                    parts = line.split(':')
                    interface_name = parts[0].strip()
                    
                    # Skip loopback interface
                    if interface_name == 'lo':
                        continue
                    
                    # Split the stats and extract received bytes (first value after the interface name)
                    stats = parts[1].strip().split()
                    if stats:
                        bytes_received = int(stats[0])
                        total_bytes_received += bytes_received
            
            download_usage[pod] = total_bytes_received
            
        except subprocess.CalledProcessError as e:
            print(f"Error executing command on pod {pod}: {e}")
            print(f"Error output: {e.stderr}")
            download_usage[pod] = -1
        except Exception as e:
            print(f"Unexpected error processing pod {pod}: {e}")
            download_usage[pod] = -1
    
    return download_usage

def get_upload_usage_per_pod():
    """
    Get upload network usage for each pod.
    
    Returns:
        dict: A dictionary mapping pod names to their upload usage in bytes
    """
    upload_usage = {}
    pods = get_list_of_pods()
    
    for pod in pods:
        try:
            # Execute kubectl exec to read network interface statistics
            result = subprocess.run(
                ["kubectl", "exec", pod, "--", "cat", "/proc/net/dev"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the output of /proc/net/dev
            # Format: Interface: Rx-bytes packets errs drop fifo frame compressed multicast Tx-bytes packets ...
            lines = result.stdout.strip().split('\n')
            
            # Skip the header lines (first two lines)
            data_lines = lines[2:]
            
            total_bytes_transmitted = 0
            
            for line in data_lines:
                # Split by colon to separate interface name from stats
                if ':' in line:
                    parts = line.split(':')
                    interface_name = parts[0].strip()
                    
                    # Skip loopback interface
                    if interface_name == 'lo':
                        continue
                    
                    # Split the stats and extract transmitted bytes (9th value after the interface name)
                    # /proc/net/dev format: receive bytes, packets, errs, drop, fifo, frame, compressed, multicast,
                    #                      transmit bytes, packets, errs, drop, fifo, colls, carrier, compressed
                    stats = parts[1].strip().split()
                    if len(stats) >= 9:  # Ensure we have enough fields
                        bytes_transmitted = int(stats[8])  # 9th field (index 8) is transmit bytes
                        total_bytes_transmitted += bytes_transmitted
            
            upload_usage[pod] = total_bytes_transmitted
            
        except subprocess.CalledProcessError as e:
            print(f"Error executing command on pod {pod}: {e}")
            print(f"Error output: {e.stderr}")
            upload_usage[pod] = -1
        except Exception as e:
            print(f"Unexpected error processing pod {pod}: {e}")
            upload_usage[pod] = -1
    
    return upload_usage

import datetime
import os

def append_net_log():
    """
    Append network usage information to the netusage.out log file.
    Format: date pod_name total_download_by_MB total_upload_by_MB
    Values are converted from bytes to megabytes and rounded to 1 decimal place.
    """
    # Get current date and time for timestamping
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Get download and upload usage data
    download_data = get_download_usage_per_pod()
    upload_data = get_upload_usage_per_pod()
    
    # Combine all pod names from both dictionaries
    all_pod_names = set(download_data.keys()) | set(upload_data.keys())
    
    # Conversion factor from bytes to megabytes
    BYTES_TO_MB = 1024 * 1024
    
    try:
        # Check if file exists to determine if we need to write a header
        file_exists = os.path.isfile('miil-pods-network-usage.out')
        
        # Open file in append mode
        with open('miil-pods-network-usage.out', 'a') as log_file:
            # Write header if file is new
            if not file_exists:
                log_file.write("date                   pod_name                total_download_MB          total_upload_MB\n")
                log_file.write("-" * 90 + "\n")
            
            # Write data for each pod
            for pod in all_pod_names:
                # Get download and upload values, default to 0 if not available
                download_bytes = download_data.get(pod, 0)
                upload_bytes = upload_data.get(pod, 0)
                
                # Skip pods with error values (-1)
                if download_bytes == -1 or upload_bytes == -1:
                    log_file.write(f"{current_time}  {pod:<20}  ERROR RETRIEVING DATA\n")
                    continue
                
                # Convert bytes to megabytes and round to 1 decimal place
                download_mb = round(download_bytes / BYTES_TO_MB, 1)
                upload_mb = round(upload_bytes / BYTES_TO_MB, 1)
                
                # Format and write the log entry
                log_file.write(f"{current_time}  {pod:<20}  {download_mb:<25.1f}  {upload_mb:<20.1f}\n")
                
        print(f"Network usage data successfully appended to netusage.out")
        
    except Exception as e:
        print(f"Error writing to log file: {e}")
        
        
if __name__ == "__main__":
    append_net_log()
