# diagnostic_env.py

import os
import sys
import platform

MAX_DIR_COUNT = 200

if __name__ == '__main__':
    try:
        print('Python version:', sys.version)
        print('Python executable:', sys.executable)
        print('Platform:', platform.platform())
        print('Current working directory:', os.getcwd())
        script_dir = os.path.dirname(os.path.abspath(__file__))
        print('Script directory:', script_dir)
        project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
        print('Project root path:', project_root)

        env_vars = ['USERNAME', 'USERPROFILE', 'HOME', 'APPDATA', 'LOCALAPPDATA', 'PROGRAMDATA', 'VIRTUAL_ENV', 'CONDA_PREFIX']
        for var in env_vars:
            print(f'{var}:', os.environ.get(var, 'Not Set'))

        path_entries = os.environ.get('PATH', '').split(os.pathsep)
        print('PATH entry count:', len(path_entries))

        try:
            dirs = [name for name in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, name))]
            print('Top-level directories (capped at 200):')
            for directory in dirs[:MAX_DIR_COUNT]:
                print(directory)
            print(f'Total directories listed: {min(len(dirs), MAX_DIR_COUNT)}')
        except PermissionError as e:
            print('PermissionError:', e)
        except Exception as e:
            print('Error listing directories:', e)
    except Exception as e:
        print('An unexpected error occurred:', e)
