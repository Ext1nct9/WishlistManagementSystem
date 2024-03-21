# Decisions

- DB file named `database.db`
- generate IDs with uuid
- salt and hash passwords in the back-end (not DB)



# How to run
- Create endpoints
- Create step definitions using behave
- pip install behave Flask requests flask-restful
- There might be version conflicts so run this if needed: pip install markupsafe==2.0.1
- Run python3 initialize_DB.py to have a database
- Run python3 app.py first to have an environment
- To use behave, run behave -t @{Add tags to scenarios that u wanna run}

# Step definitions:
- Set base_url to url of your local app
- Use logging to check for info/errors you need
- Add your databases to clean_DB.py to clean the database between runs
