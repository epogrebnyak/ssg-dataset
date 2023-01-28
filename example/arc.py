from ssg.github import *

for handle in ["facebook/docusaurus", "fastai/fastpages"]:
  r = get_repo_state_from_handle(handle)
  print(r)