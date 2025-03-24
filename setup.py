from setuptools import setup, find_packages

setup(
    name="git_diff_analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "exceptiongroup==1.2.2",
        "flake8==7.1.2",
        "iniconfig==2.1.0",
        "loging==0.0.1",
        "mccabe==0.7.0",
        "packaging==24.2",
        "pluggy==1.5.0",
        "pycodestyle==2.12.1",
        "pyflakes==3.2.0",
        "pytest==8.3.5",
        "tomli==2.2.1",
    ],
    author="Igor Amidzic",
    author_email="igorami44@gmail.com",
    description="A library to compare and identify files that were independently changed in both a remote GitHub repository branch (branchA) and a local repository branch (branchB). The library finds all files with the same path that were modified in both branches since the merge base commit, avoiding fetching branchA remotely. It uses GitHub REST or GraphQL API for remote repository requests and command-line git commands for local repository interactions.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",

    url="https://github.com/IgorAmi52/Git-Diff-Analyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
