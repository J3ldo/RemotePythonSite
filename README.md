# RemotePythonSite
A simple but effective remote python execution locked behind a password for on your server.

## What it features
* Password protection
* Changable password
* Remote python execution
* In website error logs
* Adding files
* Deleting files
* Session keys

## How to use
### Setup
The setup is fast because you dont need to do many tweaking.  
Step 1: Install the flask package using pip on to your machine.  
Step 2: Open the main.py file.  
Step 3: If its your first time opening the main.py file then put in a password.  
Step 4: Open the server using the given ip and log in with the said password.

### Executing python
Executing python is possible in the '/' route and the '/exec-python' route.  
When there you can put in the python that you want to execute and click on the execute button.  
  
Please keep in mind that when trying to put in tabs please mind that that is not possible and that you need to put in 4 spaces.  

### Changing the password
Changing your password can be done in the '/change-pass' route.  
Once there just put in your current password and your new password and click the Change Password button.  
Then if you put in the old password correct and the new passwords matched you changed your password.

### Adding files
Adding files can be done in the '/add-file' route.  
Once there you can put in the file name please keep in mind that you do need to put in the file extension (.py, .txt, .png, etc.)  
Then you kan put in the file contents and click the add file button.  

Please keep in mind that when trying to put in tabs please mind that that is not possible and that you need to put in 4 spaces.  

### Deleting files
Deleting files can be done in the '/delete-file' route.  
Once there put in the file name and extension and click the delete file. Then it will dele the file for you.

## Screenshots
### Login page
![Screenshot1](/screenshots/sc1.png)

### Main page
![Screenshot2](/screenshots/sc2.png)
