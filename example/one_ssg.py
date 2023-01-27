# pylint:disable=missing-function-docstring,missing-class-docstring,import-error

# from ssg.ssg import SSG_LIST, get_repo_state_from_handle
from ssg.ssg import from_file, to_dataframe

from random import choice

# ssg = choice(SSG_LIST)
# print(ssg)
# print(get_repo_state_from_handle(ssg.repo.handle))

ssg_list = from_file("data/ssg2.yaml")
print(ssg_list)
df = to_dataframe(ssg_list)
df.to_csv("data/ssg.csv")
