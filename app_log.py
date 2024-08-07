import subprocess
import sys
import importlib

# List of required packages (all standard libraries in this case)
required_packages = ['datetime', 'json', 're', 'os', 'webbrowser']

# Check if standard packages are available
def check_standard_packages(packages):
    for package in packages:
        try:
            importlib.import_module(package)
            print(f"Package {package} is already available.")
        except ImportError:
            print(f"Standard package {package} is missing, which is unusual for Python standard libraries.")

# Run the prettify_log script
def run_prettify_log():
    subprocess.run([sys.executable, 'prettify_log.py'])

if __name__ == '__main__':
    print("Checking required packages...")
    check_standard_packages(required_packages)
    print("All required packages are available.")
    print("Running prettify_log.py...")
    run_prettify_log()
