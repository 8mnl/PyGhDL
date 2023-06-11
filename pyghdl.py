import base64
import getopt
import os
import shutil
import sys
from typing import Optional

from github import Github, GithubException, AppAuthentication
from github.ContentFile import ContentFile
from github.Repository import Repository

from urllib.parse import urlparse

token = "YOUR_TOKEN_HERE"

def get_sha_for_tag(repository: Repository, tag: str) -> str:
    """
    Returns a commit PyGithub object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:
        raise ValueError("No Tag or Branch exists with that name")
    return matched_tags[0].commit.sha


def download_directory(repository: Repository, sha: str, server_path: str) -> None:
    """
    Download all contents at server_path with commit tag sha in the repository.
    """
    if os.path.exists(server_path):
        shutil.rmtree(server_path)

    os.makedirs(server_path)
    contents = repository.get_contents(server_path, ref=sha)

    for content in contents:
        print("Processing %s" % content.path)
        if content.type == "dir":
            os.makedirs(content.path)
            download_directory(repository, sha, content.path)
        else:
            try:
                path = content.path
                file_content = repository.get_contents(path, ref=sha)
                if not isinstance(file_content, ContentFile):
                    raise ValueError("Expected ContentFile")
                file_out = open(content.path, "w+")
                if file_content.content:
                    file_data = base64.b64decode(file_content.content)
                    file_out.write(file_data.decode("utf-8"))
                file_out.close()
            except (GithubException, IOError, ValueError) as exc:
                print("Error processing %s: %s", content.path, exc)


def main(argv):
    """
    Parses and splits the given URL arg in its parts
    (username + repository, branch, folder in repository)
    """
    url = argv[0]
    split = urlparse(url).path.split('/')
    
    repo = split[1] + "/" + split[2]
    branch = split[4]
    folder = str()

    for i in range(5, len(split)):
        if folder == str():
            folder = split[i]
        else:
            folder = folder + "/" + split[i]

    """
    Function calling
    """
    github = Github(login_or_token=token)
    repository = github.get_repo(repo)
    sha = get_sha_for_tag(repository, branch)
    print(sha)
    download_directory(repository, sha, folder)


if __name__ == "__main__":
    """
    Entrypoint - only one arg is permitted
    """
    if len(sys.argv[1:]) != 1:
        print("Please use the correct format 'python pyghdl.py <link>'")
    else:
        main(sys.argv[1:])