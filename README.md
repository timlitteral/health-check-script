# HTTP Endpoint Health Check Script
This Python script checks the health of multiple HTTP endpoints, logs their status (UP or DOWN), response times, and availability percentage. It is useful for monitoring the availability of APIs or web services.

## Requirements
- **Python**: The script is written in Python. You'll need Python 3.6 or higher installed.
- **YAML Configuration**: The endpoints and configuration are read from a YAML file named endpoints.yaml. Make sure to have a properly structured YAML file for your endpoints.

## Installation Instructions
### Step 1: Install Python
Before running the script, you must have Python installed on your computer. Follow the instructions based on your operating system below:

#### For Windows:
- Download Python from the official website: python.org
- During installation, make sure to check the box that says Add Python to PATH.
- Verify the installation by opening the Command Prompt (cmd) and typing:

    `python --version`

You should see something like `Python 3.x.x.`

#### For macOS:
If Python isn't already installed, install Homebrew (if not already installed). Run this command in your terminal:

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Install Python by running:

    brew install python

Verify the installation by typing in your terminal:

    python3 --version

#### For Linux:

Install Python using your package manager. For Ubuntu/Debian, use the following command in your terminal:

    sudo apt update
    sudo apt install python3

Verify the installation by typing:

    python3 --version

### Step 2: Install Required Dependencies

After Python is installed, you will need to install the required Python packages for the script to work.

#### For Windows:

1.  Open Command Prompt (cmd).
2.  Navigate to your script's directory:
    
    `cd C:\path\to\your\script` 
    
3.  If you have a `requirements.txt` file:
    
    `pip install -r requirements.txt` 
    
    If you don't have `requirements.txt`, you can manually install the required libraries:
    
    `pip install requests pyyaml` 
    

#### For macOS:

1.  Open Terminal.
2.  Navigate to your script's directory:
    
    `cd /path/to/your/script` 
    
3.  If you have a `requirements.txt` file:
    
    `pip3 install -r requirements.txt` 
    
    If you don't have `requirements.txt`, you can manually install the required libraries:
    
    `pip3 install requests pyyaml` 
    

#### For Linux:

1.  Open Terminal.
2.  Navigate to your script's directory:
    
    `cd /path/to/your/script` 
    
3.  If you have a `requirements.txt` file:
    
    `pip3 install -r requirements.txt` 
    
4. If you don't have `requirements.txt`, you can manually install the required libraries:
    
    `pip3 install requests pyyaml`

### Step 3: Prepare the Configuration File
The script requires a YAML configuration file that contains the list of endpoints to monitor. Create a file called endpoints.yaml with the following structure:

    - headers:
        user-agent: <your-user-agent>
      method: GET
      name: <endpoint-name-1>
      url: <endpoint-url-1>
      
    - headers:
        user-agent: <your-user-agent>
      method: GET
      name: <endpoint-name-2>
      url: <endpoint-url-2>
      
    - body: '{"key":"value"}'
      headers:
        content-type: application/json
        user-agent: <your-user-agent>
      method: POST
      name: <endpoint-name-3>
      url: <endpoint-url-3>
      
    - name: <endpoint-name-4>
      url: <endpoint-url-4>


Make sure this file is saved as endpoints.yaml in the same directory as the script.

### Step 4: Run the Script

Once everything is installed, and the configuration file is ready, you can run the script by following these steps:

#### For Windows:

1. Open Command Prompt (cmd).
2. Navigate to the directory where the script and endpoints.yaml file are located. For example:

    `cd C:\path\to\your\script`

3. Run the script with the following command:

    `python health_check.py endpoints.yaml`

#### For macOS/Linux:

1. Open Terminal.
2. Navigate to the directory where the script and endpoints.yaml file are located. For example:

    `cd /path/to/your/script`

3. Run the script with the following command:

    `python3 health_check.py endpoints.yaml`

### Step 5: View the Logs

After the script runs, it will generate logs in a file named health_check_log.txt in the same directory.
The log will show the status of each endpoint (UP or DOWN), the response time, and availability percentage.

Example of Log Output:

    2025-01-06 14:23:38.013120
    Test cycle #1 begins at time = 0 seconds:
    Endpoint with name example index page has HTTP response code 200 and response latency 100 ms => UP
    Endpoint with name example careers page has HTTP response code 403 and response latency 600 ms => DOWN (HTTP 403 Forbidden)
    example.com has 67% availability percentage

### Troubleshooting

If the script does not run, ensure Python is installed correctly and added to your system’s PATH.
    
#### For Windows:
    
1. Open **Command Prompt** and type:
        
        `python --version` 
        
If Python is correctly installed, you should see something like `Python 3.x.x`. If you see an error, you might need to add Python to your PATH.
        
#### For macOS/Linux: 
   
1. Open **Terminal** and type:
        
        `python3 --version` 
    

You should see something like `Python 3.x.x`. 

2. If you see an error, ensure Python is installed using the package manager (`brew install python` for macOS, or `sudo apt install python3` for Linux).
        
-   **If you see `ModuleNotFoundError` for `requests` or `pyyaml`**, it means the dependencies were not installed properly.
    
   **For Windows**: 

Run the following command in **Command Prompt**:
        
        `pip install requests pyyaml` 
        
  **For macOS/Linux**: 
  
Run the following command in **Terminal**:
        
        `pip3 install requests pyyaml`

### Customization
- Modify the endpoints.yaml file to include your own list of endpoints.
- You can also modify the script to customize error handling, output formatting, and more.

