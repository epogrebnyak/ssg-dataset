"""Get Github repo statistics."""

# pylint:disable=missing-function-docstring,missing-class-docstring,import-error,invalid-name

from datetime import date, datetime
from typing import Any, Dict, List, Optional

import requests
from pydantic import BaseModel

from ssg.cache import GH_TOKEN, GH_USER


def url(handle: str) -> str:
    return f"https://github.com/{handle}/"


def make_api_url(handle: str) -> str:
    return f"https://api.github.com/repos/{handle}"


def make_api_url_commits(handle: str) -> str:
    return f"https://api.github.com/repos/{handle}/commits"


# ['id', 'node_id', 'name', 'full_name', 'private', 'owner', 'html_url',
#  'description', 'fork', 'url', 'forks_url', 'keys_url', 'collaborators_url',
#  'teams_url', 'hooks_url', 'issue_events_url', 'events_url', 'assignees_url',
#  'branches_url', 'tags_url', 'blobs_url', 'git_tags_url', 'git_refs_url', 'trees_url',
#  'statuses_url', 'languages_url', 'stargazers_url', 'contributors_url', 'subscribers_url',
#  'subscription_url', 'commits_url', 'git_commits_url', 'comments_url', 'issue_comment_url',
#  'contents_url', 'compare_url', 'merges_url', 'archive_url', 'downloads_url', 'issues_url', 'pulls_url',
#  'milestones_url', 'notifications_url', 'labels_url', 'releases_url', 'deployments_url',
#  'created_at', 'updated_at', 'pushed_at', 'git_url', 'ssh_url', 'clone_url', 'svn_url',
#  'homepage', 'size', 'stargazers_count', 'watchers_count', 'language', 'has_issues',
#  'has_projects', 'has_downloads', 'has_wiki', 'has_pages', 'has_discussions',
#  'forks_count', 'mirror_url', 'archived', 'disabled', 'open_issues_count', 'license',
#  'allow_forking', 'is_template', 'web_commit_signoff_required', 'topics', 'visibility',
#  'forks', 'open_issues', 'watchers', 'default_branch', 'permissions', 'temp_clone_token',
#  'network_count', 'subscribers_count']
def get_repo(handle: str) -> Dict:
    """Query Github API and get repo information as dict."""
    response_dict = fetch(make_api_url(handle))
    if response_dict.get("message", "").startswith("API rate limit exceeded"):
        raise ValueError(response_dict)
    return response_dict


def get_commits(handle: str) -> List[Any]:
    return fetch(make_api_url_commits(handle))


def fetch(url: str, username: str = GH_USER, token: str = GH_TOKEN):
    if token:
        r = requests.get(url, auth=(username, token))
    else:
        r = requests.get(url)
    return r.json()


def last_modified(handle: str) -> str:
    _last = get_commits(handle)[0]
    return _last["commit"]["author"]["date"]


def date_only(ts: str) -> date:
    """Extract date from *ts* timestamp.

    Timestamp has YYYY-mm-ddTHH:MM:SSZ format.
    """
    # must to strip 'Z' first as discussed in https://discuss.python.org/t/parse-z-timezone-suffix-in-datetime/2220
    return datetime.fromisoformat(ts.rstrip("Z")).date()


class RepoState(BaseModel):
    repo_lang: str
    url: str
    # some repos do not have webpage, e.g. https://github.com/alexkorban/elmstatic
    homepage: Optional[str]
    created: date
    modified: date
    stars: int
    forks: int
    open_issues: int
    is_archived: Optional[bool] = None


def get_repo_state_from_handle(handle: str) -> RepoState:
    """Return Github repo statistics by repo handle.

    Example:

       get_repo_state_from_handle("withastro/astro")

    returns

    ```
    RepoState(
        repo_lang="TypeScript",
        url="https://github.com/withastro/astro/",
        homepage="https://astro.build",
        created="2021-03-15",
        modified="2022-06-19",
        stars=12422,
        forks=641,
        open_issues=98,
    )
    ```
    """
    print("Retrieving data for", handle, "...")
    repo = get_repo(handle)
    return RepoState(
        repo_lang=repo["language"],
        url=url(handle),
        homepage=repo["homepage"],
        created=date_only(repo["created_at"]),
        modified=date_only(last_modified(handle)),
        stars=int(repo["stargazers_count"]),
        forks=int(repo["forks_count"]),
        open_issues=int(repo["open_issues_count"]),
        is_archived=repo["archived"],
    )
