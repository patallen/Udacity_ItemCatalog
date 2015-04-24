##Video Game Catalog Project
This is the third final project for the Udacity Full Stack NanoDegree.

##Instructions
1. Clone repo: `git clone https://github.com/patallen/Udacity_ItemCatalog`
2. Install requirements: `pip install -r requirements.txt`
3. Create Database: `python fill_db.py`
4. Add your own client secrets information:
	- Create a project at console.developers.google.com
	- Once created, click on ```download json```
	- place it in the root directory of this project as "client_secrets.json"
	- Finally, in login.html, change the data-client attribute of the signinButton to reflect your client ID.
5. Start the webserver: `python run.py`
6. Open browser and navigate to http://localhost:8000/
