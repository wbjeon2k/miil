#!/usr/bin/env python3

import os
import subprocess
import datetime
import yaml
import re

def get_user_input(prompt, validate_func=None, error_message=None, default_value=None):
    """Get user input with optional validation and default value"""
    while True:
        user_input = input(prompt)
        
        # Use default value if input is empty
        if not user_input and default_value is not None:
            return default_value
            
        if validate_func is None or validate_func(user_input):
            return user_input
        
        if default_value is not None:
            print(f"{error_message or 'Invalid input.'} Using default value: {default_value}")
            return default_value
        
        print(error_message or "Invalid input. Please try again.")

def validate_username(username):
    """Validate username format"""
    return bool(re.match(r'^[a-zA-Z0-9_-]+$', username))

def validate_docker_hub_path(path):
    """Validate Docker Hub path format"""
    # Empty input will be handled separately
    if not path:
        return False
    # Basic validation for a Docker image path
    return bool(re.match(r'^[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.-]+$', path))

def validate_num_gpus(num_gpus):
    """Validate number of GPUs"""
    try:
        num = int(num_gpus)
        return 1 <= num <= 8  # Assuming a reasonable range
    except ValueError:
        return False

def main():
    print("=== Kubernetes Pod Creation Tool ===")
    
    # Define default Docker Hub path
    DEFAULT_DOCKER_PATH = "login.local:8888/ost-hub/cuda12.1-pytorch2.3-py3.10:2024-05-01"
    
    # Get user inputs
    username = get_user_input(
        "Enter your username: ", 
        validate_username, 
        "Username must contain only alphanumeric characters, underscores, and hyphens."
    )
    
    docker_hub_path = get_user_input(
        "Enter Docker Hub image path (or press Enter for default): ", 
        validate_docker_hub_path,
        "Invalid Docker image path.",
        DEFAULT_DOCKER_PATH
    )
    
    num_gpus = get_user_input(
        "Enter number of GPUs required: ", 
        validate_num_gpus,
        "Number of GPUs must be a positive integer between 1 and 8."
    )
    
    # Generate current date in YYYYMMDD format
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    
    # Read the YAML template
    with open('pod_template.yaml', 'r') as file:
        template_content = file.read()
    
    # Create the custom password based on username
    custom_password = f"miil@{username.lower()}"
    
    # Replace the default password in the template
    template_content = template_content.replace("echo 'root:sshsecret2024' | chpasswd", 
                                             f"echo 'root:{custom_password}' | chpasswd")
    
    # Also update the echo message that displays the password
    template_content = template_content.replace("echo \"SSH server starting - root password is 'sshsecret2024'\"", 
                                             f"echo \"SSH server starting - root password is '{custom_password}'\"")
    
    # Replace other placeholders
    yaml_content = template_content.replace('{USERNAME}', username.lower())
    yaml_content = yaml_content.replace('{DATE YYYYMMDD}', current_date)
    yaml_content = yaml_content.replace('{DOCKERHUBPATH}', docker_hub_path)
    yaml_content = yaml_content.replace('{NUMGPUS}', num_gpus)
    
    # Generate output filename
    output_filename = f"miil-{username.lower()}-{current_date}.yaml"
    
    # Write the filled template to a file
    with open(output_filename, 'w') as file:
        file.write(yaml_content)
    
    print(f"\nYAML file created: {output_filename}")
    print(f"Docker image path used: {docker_hub_path}")
    print(f"SSH root password set to: {custom_password}")
    
    # Ask user if they want to apply the configuration
    apply_config = get_user_input("Do you want to apply this configuration? (y/n): ")
    
    if apply_config.lower() in ['y', 'yes']:
        try:
            # Apply the YAML file using kubectl
            subprocess.run(["kubectl", "apply", "-f", output_filename], check=True)
            print(f"\nPod created successfully!")
            
            # Provide some helpful information
            print(f"\nTo check pod status:")
            print(f"kubectl get pod miil-{username.lower()}-{current_date} -n miil")
            print(f"\nTo get pod logs:")
            print(f"kubectl logs miil-{username.lower()}-{current_date} -n miil")
            print(f"\nTo delete the pod:")
            print(f"kubectl delete pod miil-{username.lower()}-{current_date} -n miil")
            print(f"\nSSH into the pod with password '{custom_password}':")
            print(f"kubectl exec -it miil-{username.lower()}-{current_date} -n miil -- /bin/bash")
            
        except subprocess.CalledProcessError as e:
            print(f"\nError creating pod: {e}")
            print("You may want to check if the namespace exists or if you have the right permissions.")
    else:
        print("\nConfiguration was not applied. You can apply it manually using:")
        print(f"kubectl apply -f {output_filename}")

if __name__ == "__main__":
    main()
