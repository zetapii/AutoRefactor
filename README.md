## Automated Refactoring Pipeline 

This project is a Python application designed to improve code quality in GitHub repositories by identifying design smells, refactoring code, and creating pull requests with the refactored code.

### Configuration

To configure the application, follow these steps:

1. Create a `.env` file in the root directory of your project.

2. Add the following environment variables to the `.env` file:

    ```plaintext
    GITHUB_OWNER=yourusername
    GITHUB_REPO_NAME=your-repo-name
    GITHUB_TOKEN=your-github-token
    OPENAI_TOKEN=your-OpenAI-token
    SCAN_INTERVAL=scan-interval-in-seconds

    ```

    Replace `yourusername`, `your-repo-name`, `your-github-token`, and `scan-interval-in-seconds` with your GitHub username, the name of the repository you want to scan, your GitHub personal access token, and the interval at which you want to scan the repository, respectively.

### Running the Application

To run the application:

1. Navigate to the project directory in your terminal.

2. Run the following command:

    ```plaintext
    python3 scanner.py
    ```

    This command starts the application, initiating the scanning process for the specified GitHub repository to detect and refactor design smells in Python code.

### Components

The application consists of the following components:

- **DesignMetric Class:** This class is responsible for identifying design smells in Python code.
- **OpenAIRefactorer Class:** It handles the refactoring of code using OpenAI's code refactoring capabilities.
- **AutoPR Class:** This class automates the process of creating pull requests with the refactored code.

### Note

Ensure that you have appropriate permissions and access rights to the GitHub repository specified in the configuration.
