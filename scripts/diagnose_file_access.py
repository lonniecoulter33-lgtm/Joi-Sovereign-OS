#!/usr/bin/env python3

import os
import sys
import platform
import tempfile
import traceback


def check_environment():
    results = {}
    try:
        results['python_version'] = sys.version
        results['executable'] = sys.executable
        results['platform'] = platform.platform()
        results['cwd'] = os.getcwd()
        results['project_root'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    except Exception as e:
        results['environment_error'] = str(e)
        results['environment_traceback'] = traceback.format_exc()
    return results


def check_directories(project_root):
    results = {}
    try:
        modules_dir = os.path.join(project_root, 'modules')
        plugins_dir = os.path.join(project_root, 'plugins')
        results['modules_exists'] = os.path.exists(modules_dir)
        if results['modules_exists']:
            results['modules_list'] = os.listdir(modules_dir)
        results['plugins_exists'] = os.path.exists(plugins_dir)
        if results['plugins_exists']:
            results['plugins_list'] = os.listdir(plugins_dir)
    except Exception as e:
        results['directory_error'] = str(e)
        results['directory_traceback'] = traceback.format_exc()
    return results


def check_file_read(project_root):
    results = {}
    file_path = os.path.join(project_root, 'joi_companion.py')
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                results['file_read'] = f.read(100)  # Read first 100 characters
        else:
            results['file_read_error'] = 'File not found'
    except Exception as e:
        results['file_read_error'] = str(e)
        results['file_read_traceback'] = traceback.format_exc()
    return results


def check_file_write_delete(project_root):
    results = {}
    temp_filename = 'temp_test_file.txt'
    temp_file_path = os.path.join(project_root, temp_filename)
    temp_system_path = os.path.join(tempfile.gettempdir(), temp_filename)
    try:
        # Test write/delete in project root
        with open(temp_file_path, 'w') as f:
            f.write('test')
        os.remove(temp_file_path)
        results['project_root_write_delete'] = 'Success'
    except Exception as e:
        results['project_root_write_delete_error'] = str(e)
        results['project_root_write_delete_traceback'] = traceback.format_exc()
    try:
        # Test write/delete in system temp directory
        with open(temp_system_path, 'w') as f:
            f.write('test')
        os.remove(temp_system_path)
        results['temp_dir_write_delete'] = 'Success'
    except Exception as e:
        results['temp_dir_write_delete_error'] = str(e)
        results['temp_dir_write_delete_traceback'] = traceback.format_exc()
    return results


def run_diagnostics():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    environment_results = check_environment()
    directory_results = check_directories(project_root)
    file_read_results = check_file_read(project_root)
    file_write_delete_results = check_file_write_delete(project_root)

    all_results = {
        'environment': environment_results,
        'directories': directory_results,
        'file_read': file_read_results,
        'file_write_delete': file_write_delete_results,
    }

    for category, results in all_results.items():
        print(f"\n{category.upper()} CHECK:")
        for key, value in results.items():
            print(f"{key}: {value}")

    # Determine exit code
    exit_code = 0
    for results in all_results.values():
        for value in results.values():
            if 'error' in value:
                exit_code = 1
                break

    sys.exit(exit_code)


if __name__ == '__main__':
    run_diagnostics()