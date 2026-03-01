#!/usr/bin/env python
import sys
import os
import platform
import json
import datetime

# List of environment variables to include in the report
ENV_VARS = ['PATH', 'HOME', 'USER', 'SHELL', 'PYTHONPATH']

# Function to redact sensitive information from environment variables
def redact_env_var(var_name, var_value):
    # Example: redact user names or any sensitive info
    if 'SECRET' in var_name.upper():
        return 'REDACTED'
    return var_value

# Function to gather environment information
def gather_env_info():
    env_info = {
        'python_version': sys.version,
        'python_executable': sys.executable,
        'os_name': os.name,
        'platform_system': platform.system(),
        'platform_release': platform.release(),
        'sys_path': sys.path,
        'current_working_directory': os.getcwd(),
        'user': os.getenv('USER') or os.getenv('USERNAME'),
        'timestamp': datetime.datetime.now().isoformat(),
        'environment_variables': {var: redact_env_var(var, os.getenv(var)) for var in ENV_VARS if os.getenv(var) is not None}
    }
    return env_info

# Main function to print the environment information
def main():
    env_info = gather_env_info()
    if '--json' in sys.argv:
        print(json.dumps(env_info, indent=4))
    else:
        for key, value in env_info.items():
            if isinstance(value, dict):
                print(f"{key}:")
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"{key}: {value}")

if __name__ == '__main__':
    main()
