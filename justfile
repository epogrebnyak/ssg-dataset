package := "ssg"

# List available commands 
list:
   just --list

# launch streamlit app
st:
  poetry run streamlit run streamlit_app.py

# black and isort
lint:  
   black .
   isort .

# build documentation 
docs:
  poetry run sphinx-build -a docs docs/site

# show documentation in browser
show:
  start docs/site/index.html

# publish documentation to Github Pages
pages:
  poetry run ghp-import docs/site 

# create rst source for API documentation
apidoc:
  sphinx-apidoc -o docs src/{{package}}

# update csv file (project-specific) 
update:
  poetry run python example/update.py

# print table for README file (project-specific)
table:
  poetry run python example/table.py
          