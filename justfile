package := "ssg"

# List available commands 
list:
   just --list

# Launch Streamlit app
app:
  poetry run streamlit run app/Static_site_generators.py

# Use black and isort
lint:  
   black .
   isort .

# Build documentation files
docs-build:
  poetry run sphinx-build -a docs docs/site

# Show documentation in browser
docs-show:
  python -m http.server -d docs/site  

# Publish documentation to Github Pages
docs-publish:
  poetry run ghp-import docs/site 

# Create RST source file for API documentation
docs-create:
  poetry run sphinx-apidoc -o docs src/{{package}}

# Create new CSV file, patch version and make release
update-full:
  just update
  just patch
  just release

# Create new CSV file and SVG badge
update:
  poetry run python example/update.py
  just badge
  
# Bump 0.0.x version number
patch:
  poetry version patch  

# Make Github release using version from poetry.toml  
release:
  just version | xargs -I % gh release create %   

# Run pytest and pyright
test:
  poetry run pytest
  poetry run pyright src

# Run precommit hook
precommit:
  pre-commit run --all-files

# Show package version
version:
  poetry version -s | tr -d '\r' | xargs -I % echo v%

# Create brightgreen SVG badge with SSG count  
badge:   
  wc -l data/ssg.csv | xargs -I % npx badge SSG % :brightgreen > app/ssg_count.svg

# Run prettier on markdown files
prettier:
  npx prettier *.md --write