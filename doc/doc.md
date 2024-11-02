# Auto Refactor

### 

---

## Introduction

This project is a `Python-Based Application` designed to automatically scan a GitHub repository, identify `Python` files with design smells, refactor the code using OpenAI's GPT-3.5 model, and create a pull request with the refactored code.Note that our code only Python files are refactored , as their abstract syntax tree are easily iterable which is very helpful to calculate code metrics.

The application is built around the `Scanner` class, which takes the owner of the repository, the repository name, and an authentication token as inputs. It uses the `DesignMetric` class to identify design smells, the `OpenAIRefactorer` class to refactor the code, and the `AutoPR` class to create pull requests.

**Assumptions and Notes**

1. The application currently supports only Python files. Files in other languages will be ignored.
2. **The application ensures that refactoring is correct in syntax** by leveraging Python's abstract syntax tree (AST) to parse and validate the code returned by GPT 3.5. If the code cannot be correctly parsed into an AST, the script makes GPT request again to ensure that code returned is correct.
3. **The application ensures that refactoring eliminates smell by** running the metric again after getting the refactored code , and pull request is created only after getting the refactored code with eliminated design smell.**Five** retries are made to get correct response from GPT-3.5 , this can be increased to get better performance , however API usage limit of OpenAI should be kept in mind.
4. **The application refactors one file at a time** 
5. The application refactors the following design smell :
    - **Insufficient Modularization**(Having Long Methods)
    - **Insufficient Abstraction**(Causing High Cyclomatic Complexity)

## Automated Refactoring Pipeline

Concise Visualisation of the script, some details have been removed for clarity 

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled.png)

| Responsibility | Class Used | Comments |
| --- | --- | --- |
| **Automated Design Smell Detection** | **DesignMetric** | This class calculates the code metric , failing the code metric will trigger the automated refactoring pipeline to refactor the corresponding file which failed.See below table for design smell and metric mapping. |
| **Automated Refactoring** | **OpenAIRefactorer** | External API call is made to OpenAI GPT-3.5 |
| **Pull Request Generation**
 | **AutoPR** | PyGithub APIs are used to create pull request for the refactored code |

| Design Smell | Metric Used |
| --- | --- |
| **Insufficient Modularization** | Number of executable statements of a method or class ( excludes comments and empty lines) |
| **Insufficient Abstraction** | Cyclomatic Complexity = **E – N + 2P**, where E corresponds to edges, N to nodes, and P to connected components |

We now provide description of all the classes used : 

### **Class: CyclomaticComplexityVisitor**

The `CyclomaticComplexityVisitor` class is an extension of the `ast.NodeVisitor` class, which is part of Python's `ast` module. The `ast.NodeVisitor` class is typically used for traversing and modifying nodes in an Abstract Syntax Tree (AST). In this context, the `CyclomaticComplexityVisitor` class is specifically designed to calculate the cyclomatic complexity of a given piece of code, which is a crucial metric in software development.

Cyclomatic complexity is a quantitative measure of the number of linearly independent paths through a program's source code. It is computed using the control flow graph of the program. In the `CyclomaticComplexityVisitor` class, each `if` (and `else if`) condition represents a decision point in the code, thereby increasing the cyclomatic complexity by one. However, it's important to note that the `else` condition does not increment the cyclomatic complexity as its contribution is already counted by the corresponding if.

### **Class: DesignMetric**

The `DesignMetric` class provides methods to analyze a piece of code for certain design metrics. It uses Python's `ast` module to parse the code into an abstract syntax tree (AST) and then traverses the tree to calculate the metrics.

**Methods:**

- `find_long_methods(self, code, max_lines=30)`: This method **returns** methods in the code that exceed a specified length. It takes two parameters:
    - `code`: A string representing the code to be analyzed.
    - `max_lines`: An integer representing the maximum acceptable length of a method. The default value is 30.
    
    The method parses the code into an AST and then uses a nested `MethodVisitor` class to traverse the tree. The `MethodVisitor` class extends `ast.NodeVisitor` and overrides the `visit_FunctionDef` method to check the length of each function in the code. If a function exceeds `max_lines`, its name is added to the `long_methods` list. The `find_long_methods` method then returns this list.
    
- `calculate_cyclomatic_complexity(self, code)`: This method **returns** the cyclomatic complexity of the code. It takes one parameter:
    - `code`: A string representing the code to be analyzed.
    
    The method parses the code into an AST and then uses an instance of the `CyclomaticComplexityVisitor` class to traverse the tree and calculate the complexity. The calculated complexity is then returned.
    

### **Class: OpenAIRefactorer**

The `OpenAIRefactorer` class uses OpenAI's GPT-3 model to refactor Python code that has been identified to have design smells. It interacts with the OpenAI API to generate refactored code.

**Attributes:**

- `api_key`: A string representing the OpenAI API key. If not provided, it will be fetched from the environment variable "OPENAI_TOKEN".
- `client`: An `OpenAI` object initialized with the API key.

**Methods:**

- `refactor_code(self, code, design_smells)`: This method takes in the original code and the identified design smells as input, and returns the refactored code. It constructs a prompt for the OpenAI API, which includes the original code and the design smells. The API response is then parsed to extract the refactored code. If the refactored code is invalid Python code, the method retries the refactoring process with a slightly modified prompt. If the refactored code is still invalid after the retry, an exception is raised.
- `filter_to_python_code(self, input_code)`: This method takes a string of code as input and returns a cleaned version of the code with newline character and ensuring correct indentation . This is significant part for preprocessing, ensuring that the code can be correctly parsed by Python's `ast` module to calculate metrics .
- `invalid_python_code(self, code)`: This method checks if a string of code is valid Python code. It attempts to parse the code using Python's `ast` module. If a `SyntaxError` is raised during parsing, the method returns `True`, indicating that the code is invalid. Otherwise, it returns `False`, indicating that the code is valid.

### **Class: AutoPR**

The `AutoPR` class is designed to automate the process of creating pull requests on GitHub. This is a crucial part of the auto-refactoring pipeline as it totally automates the pull request creation part

**Attributes:**

- `token`: A string representing the GitHub token for authentication. If not provided, it will be fetched from the environment variable "GITHUB_TOKEN".
- `auth`: An `Auth.Token` object created using the GitHub token.
- `g`: A `Github` object initialised with the authentication object.

**Methods:**

- `create_pull_request(self, owner, repo, branch_name, title, body, file_path, content)`: This method creates a pull request in the specified repository with the updated file content.**branch_name** is the name of the branch which will be created to resolve the issue and create pull request.

### **Class: Scanner**

This class orchestrates the scanning of GitHub repositories for design smells and triggers refactoring actions.

The `Scanner` class is designed to scan a GitHub repository periodically, identify Python files with design smells, refactor the code using OpenAI's GPT-3 model, and create a pull request with the refactored code.

**Attributes:**

- `owner`: A string representing the owner of the GitHub repository.
- `repo_name`: A string representing the name of the GitHub repository.
- `auth_token`: A string representing the GitHub authentication token.
- `metric`: An instance of the `DesignMetric` class used to identify design smells.
- `refactorer`: An instance of the `OpenAIRefactorer` class used to refactor the code.
- `autoPR`: An instance of the `AutoPR` class used to create pull requests.

**Methods:**

- `__init__(self, owner, repo_name, auth_token)`: Initializes the `Scanner` object with the provided owner, repository name, and authentication token.
- `scan_github_file(self, item)`: This method scans a single file from the GitHub repository. It first checks if the file is a Python file. If it is, it retrieves the file content, identifies design smells, refactors the code if necessary, and creates a pull request with the refactored code.
- `scan_github_repo(self)`: This method scans the entire GitHub repository. It retrieves the contents of the repository and calls `scan_github_file` for each item in the contents.

## Working Example

We will show one working example in the below snippets , `complex_operations.py` has **Insufficient Modularization** Design Smell because of long method.

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled%201.png)

Design Smell Detection

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled%202.png)

Automatic PR Generation 

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled%203.png)

Description is provided in the pull request ,  functions which were causing Design Smell are listed 

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled%204.png)

Initial Code Snippet

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled%205.png)

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled%206.png)

Code Refactored By GPT 3.5 API 

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled%207.png)

![Untitled](Auto%20Refactor%20c6cec6c469c04140978bb35d0b0908e1/Untitled%208.png)