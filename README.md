Steps to Deploy the website using the Gunicorn
1. Update the requirements.txt file
2. Add Procfile 
   web: gunicorn main:main      add new this command in that file
3. Add .env file at top level
4. Add .gitignore file at top level
5. Change the debugger to false
6. Add and install gunicorn packege in your project as well as in requirements 
7. 