from github import Auth,Github
import os
from dotenv import load_dotenv

#AutoPR class is used to create pull request in the github repository by using the github token
class AutoPR:
    def __init__(self, token=None,default_commit_message="rectified design smell"):
        load_dotenv()
        self.token = os.getenv("GITHUB_TOKEN") if token is None else token
        self.auth = Auth.Token(self.token)
        self.g = Github(auth=self.auth)
        self.default_commit_message = default_commit_message

    def create_pull_request(self, owner, repo, branch_name, title, body, file_path, content):
        self.repo = self.g.get_repo(owner+"/"+repo)
        self.file = self.repo.get_contents(file_path,ref = "master")
        self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=self.repo.get_branch("master").commit.sha)
        self.repo.update_file(self.file.path, self.default_commit_message , content, self.file.sha, branch_name)    
        self.repo.create_pull(base="master", head=branch_name, title = title, body = body)

#Basic test cases for the AutoPR class
def test_AutoPR():
    autoPR = AutoPR()
    owner = "zetapii"
    repo = "SE-Project1-Test"
    branch_name = "modified_branch"
    title = "design smell rectification"
    body = "this changed the design smell of long method"
    file_path = "test.txt" 
    content = "This is the updated content which rectified design smell" 
    autoPR.create_pull_request(owner, repo, branch_name, title, body, file_path, content)

if __name__ == "__main__":
    test_AutoPR()