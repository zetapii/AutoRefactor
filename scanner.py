import requests
import base64
from metric import DesignMetric
from refactorer import OpenAIRefactorer 
from AutoPR import AutoPR
import time 
from dotenv import load_dotenv
import os 

#Scanner class is used to scan the github repository for the design smells and create pull request for the same
#It uses the DesignMetric class to find the design smells and OpenAIRefactorer class to refactor the code
#It uses the AutoPR class to create pull request in the github repository
class Scanner:
    def __init__(self, owner, repo_name, auth_token):
        self.owner = owner
        self.repo_name = repo_name
        self.auth_token = auth_token
        self.metric = DesignMetric()
        self.refactorer = OpenAIRefactorer()
        self.autoPR = AutoPR()
    #scan_github_file is used to scan the github python file for the design smells and create pull request for the same
    def scan_github_file(self , item ):
        headers = {'Authorization': f"token {self.auth_token}" if self.auth_token else None}
        if item['type'] == 'file' and item['name'].endswith('.py'):
            file_path = item['path']
            file_url = f"https://api.github.com/repos/{self.owner}/{self.repo_name}/contents/{file_path}"
            file_response = requests.get(file_url, headers=headers)
            if file_response.status_code == 200:
                file_data = file_response.json()
                file_content = base64.b64decode(file_data['content']) 
                if isinstance(file_content, bytes):
                    file_content = file_content.decode('utf-8')
                code = self.refactorer.filter_to_python_code(file_content)
                if self.metric.find_long_methods(code):
                    print("Long methods detected. Refactoring...")
                    refactored_code = self.refactorer.refactor_code(code, "Long method Design smell")
                    print(f"Refactored code:\n{refactored_code}")
                    for _ in range(5):
                        if not self.metric.find_long_methods(refactored_code):
                            break
                        refactored_code = self.refactorer.refactor_code(code, "Long method Design smell")
                    timestamp = int(time.time())
                    branch_name = f"InsufficientModulrazationDesignSmell-{timestamp}"
                    long_methods = self.metric.find_long_methods(code)
                    body = "**Refactoring Summary:**\n"
                    body += "- Added more modularization , below methods were causing design smell:\n"
                    for method in long_methods:
                        body += f"  * {method}\n"
                    self.autoPR.create_pull_request(self.owner, self.repo_name, branch_name, "Refactoring Insufficient Modularization - Long Method",body,file_path, refactored_code)
                elif self.metric.calculate_cyclomatic_complexity(code) > 10:
                    print("Cyclomatic complexity is high. Refactoring...")
                    refactored_code = self.refactorer.refactor_code(code, "Cyclomatic Complexity too many conditional statements Design smell")
                    for _ in range(5):
                        if self.metric.calculate_cyclomatic_complexity(refactored_code) <= 10:
                            break
                        refactored_code = self.refactorer.refactor_code(code, "Cyclomatic Complexity too many conditional statements Design smell")
                    timestamp = int(time.time())
                    branch_name = f"CyclomaticComplexityDesignSmell-{timestamp}"
                    body = "Refactoring Summary:\n"
                    body += "Optimised Conditional statements to reduce Design smells\n"
                    print(f"Refactored code:\n{refactored_code}")
                    self.autoPR.create_pull_request(self.owner, self.repo_name, branch_name, "Refactoring Insufficient Abstraction - Cyclomatic Complexity",body,file_path, refactored_code)
                else:
                    print("No design smells detected.")
            else : 
                print(f"Failed to retrieve file {file_path}. Status code: {file_response.status_code}")

    #scan_github_repo is used to scan the github repository for the python files and extract their contents and call the scan_github_file method
    def scan_github_repo(self):
        """
        Scans a GitHub repository for Python files and extracts their contents.

        Args:
            owner (str): The owner of the repository.
            repo_name (str): The name of the repository.
            auth_token (str, optional): A GitHub personal access token for private repositories. Defaults to None.

        Returns:
            None
        """

        api_url = f"https://api.github.com/repos/{self.owner}/{self.repo_name}/contents"
        headers = {'Authorization': f"token {self.auth_token}" if self.auth_token else None}
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            contents = response.json()
            for item in contents:
                self.scan_github_file(item)
        else:
            print(f"Failed to retrieve repository contents. Status code: {response.status_code}")

def main():
    load_dotenv()
    owner = os.getenv('GITHUB_OWNER')
    repo_name = os.getenv('GITHUB_REPO_NAME')
    auth_token = os.getenv('GITHUB_TOKEN')
    try: 
        sc = Scanner(owner, repo_name, auth_token)
        sc.scan_github_repo()
        time.sleep(int(os.getenv('SCAN_INTERVAL')))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()