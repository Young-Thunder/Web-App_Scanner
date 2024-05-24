For Windows

Step 1: Install Python
Download Python:

Go to python.org.
Click on the "Download Python" button.
Run the Installer:

Open the downloaded installer.
Make sure to check the box "Add Python to PATH".
Click "Install Now" and follow the prompts to complete the installation.
Step 2: Install Nuclei
Download Nuclei:

Go to the Nuclei Releases page.
Download the latest nuclei-windows-amd64.zip.
Extract Nuclei:

Extract the downloaded nuclei-windows-amd64.zip file.
Move the nuclei.exe file to a directory that is included in your system's PATH. You can use C:\Windows\System32 or create a new directory (e.g., C:\Nuclei) and add it to your PATH.
Add Nuclei to PATH (if needed):

Press Win + X and select System.
Click on "Advanced system settings".
In the System Properties window, click on the "Environment Variables" button.
In the Environment Variables window, find the "Path" variable in the "System variables" section, and click "Edit".
Click "New" and add the path to the directory where you moved nuclei.exe (e.g., C:\Nuclei).
Click "OK" to close all windows.
Step 3: Create and Save the Python Script
Open a Text Editor:

Open Notepad or any other text editor of your choice.
Copy the Script:
Save the Script:
Save the file with the name vcs_scanner.py in a location you can easily access (e.g., your Desktop or Documents folder).


Open Command Prompt:

Press Win + R, type cmd, and press Enter.
Navigate to the Script Location:

Use the cd command to navigate to the directory where you saved vcs_scanner.py

and run the file. 
