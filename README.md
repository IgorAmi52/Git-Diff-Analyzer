# File Change Detection Library

This project is a Python library that detects and compares file changes in two branches (`branchA` on GitHub remote repository and `branchB` locally). It identifies files that have been modified independently in both branches since their merge base commit. The library avoids fetching `branchA` and focuses on comparing changes remotely and locally.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
   - [Remote GitHub Repository Setup](#remote-github-repository-setup)
   - [Local Repository Setup](#local-repository-setup)
3. [Features](#features)
4. [License](#license)

## Installation

### Prerequisites  
- Python 3.x
- `pip` and `build` installed
- Git installed on your system  
- A GitHub personal access token  

1. Clone this repository:
    ```bash
    git clone https://github.com/IgorAmi52/Git-Diff-Analyzer.git
    cd Git-Diff-Analyzer
    ```
### Building the Package  

To package the project for distribution:  

1. **Ensure `build` is installed:**  
    ```bash
    pip install --upgrade build
    ```

2. **Build the package:**  
    ```bash
    python -m build -w
    ```

This will generate a `.whl` file inside the `dist/` directory.

### Installing from Built Package  

To install the built package:  

```bash
pip install dist/git_diff_analyzer-0.1.0-py3-none-any.whl
```
## **Usage**  

This library compares files between a **remote GitHub repository (`branchA`)** and a **local repository (`branchB`)** based on their merge base commit.  

### Remote GitHub Repository Setup  
- Ensure you have a **GitHub Personal Access Token (PAT)** with read permissions.  
- The repository must be **accessible** via GitHub's REST API.  

### Local Repository Setup
- Ensure you have a **local clone** of the repository.  
- The local repository should have **both `branchA` (fetched remotely) and `branchB` (created locally)**.  

### **Import and Use `compare_local_remote_changes`**  

#### **Example: Comparing Changed Files**  
```python
from git_diff_analyzer import compare_local_remote_changes

# Configuration
owner = "your-username"
repo = "your-repo"
access_token = "your-github-token"
local_repo_path = "/path/to/local/repo"
branchA = "main"
branchB = "feature-branch"

# Compare changes between remote branchA and local branchB
changed_files = compare_local_remote_changes(owner, repo, access_token, local_repo_path, branchA, branchB)

# Output results
print("Files changed in both branches independently:", changed_files)
```

If there are files that were changed independently in both (`branchA`) (remotely) and (`branchB`(locally) since their merge base, the script will print:

```bash
Files changed in both branches independently: ['file1.txt', 'src/module.py']
```

## Features

- **Changed File Detection**: Detects files that have been modified on both the remote (`branchA`) and local (`branchB`) repositories since their common merge base commit.
- **File Filtering**: Removes files that have been reverted to the same state in both repositories.
- **Diff Calculation**: Compares files between commits and branches, ensuring only the relevant files are considered.
- **Logging**: Logs events and errors for better traceability.


## License

This project is licensed under the MIT License.