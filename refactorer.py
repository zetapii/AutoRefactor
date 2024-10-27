from openai import OpenAI
import ast
from dotenv import load_dotenv
import os

# OpenAIRefactorer class is used to refactor the code by using the openAI API
class OpenAIRefactorer:
    #api_key is the key to access the openAI API
    def __init__(self,api_key = None):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_TOKEN") if api_key is None else api_key
        self.client = OpenAI(api_key=self.api_key)

    def refactor_code(self, code, design_smells):
        prompt = f"Given the following code:\n\n{code}\n\nIdentified design smells:\n{design_smells}\n\nRefactor the code to eliminate the design smells:"

        response = self.client.chat.completions.create(
            messages=[{"role": "system", "content": prompt}],
            model="gpt-3.5-turbo"
        )
        refactored_code = response.choices[0].message.content.strip()
        if self.invalid_python_code(refactored_code):
            prompt = f"Given the following code:\n\n{code}\n\nIdentified design smells:\n{design_smells}\n\n .Don't include any explanation in your response , only respond with code.Refactor the code to eliminate the design smells: "
            response = self.client.chat.completions.create(
                messages=[{"role": "system", "content": prompt}],
                model="gpt-3.5-turbo"
            )
            refactored_code = response.choices[0].message.content.strip()
        if self.invalid_python_code(refactored_code):
            raise Exception("Refactored code is invalid python code")
        return refactored_code
    
    #filter_to_python_code is used to remove the newline characters and common indentation from the code
    def filter_to_python_code(self,input_code):
        lines = input_code.split('\n')
        #wrap it up in try except block to handle the case if the code is not a valid python code
        try:
            common_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())
            cleaned_lines = [line[common_indent:] for line in lines]
            python_code = '\n'.join(cleaned_lines)
            return python_code 
        except : 
            print("Invalid python code / Empty Code")
            return ""

    #invalid_python_code is used to check the case if the code is an invalid python code 
    def invalid_python_code(self,code):
        try:
            ast.parse(code)
        except SyntaxError:
            return True
        return False


#Basic test cases for the OpenAIRefactorer class
def test_OpenAIRefactorer():
    refactorer = OpenAIRefactorer()
    code = """
def my_function(x):
    if x > 0:
        print("x is positive")
    elif x == 0:
        print("x is zero")
    elif x == 4:
        print("x is non-positive")
    else:
        if x > 0:
            print("x is positive")
        elif x == 0:
            print("x is non-positive")
        elif x == 4:
            print("x is non-positive")
            print("x is negative")
            print("hi")
"""
    design_smells = "Nested if statements, lack of comments"
    refactored_code = refactorer.refactor_code(code, design_smells)
    print("Refactored code:\n", refactored_code)


if __name__ == "__main__":
    test_OpenAIRefactorer()