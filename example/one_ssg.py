# pylint:disable=missing-function-docstring,missing-class-docstring,import-error

from ssg.ssg import SSG_LIST, get_repo_state_from_handle

from random import choice

ssg = choice(SSG_LIST)
print(ssg)
print(get_repo_state_from_handle(ssg.repo.handle))
