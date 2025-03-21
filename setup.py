from setuptools import setup, find_packages

setup(
    name="git-diff-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'GitPython',  # Add any other dependencies you're using
    ],
    author="Igor Amidzic",
    description="A tool for analyzing git diffs between local and remote branches",
    python_requires=">=3.6",
)
