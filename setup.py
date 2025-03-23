from setuptools import setup, find_packages

setup(
    name="git-diff-analyzer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    author="Igor Amidzic",
    description="A tool for analyzing git diffs between local and remote branches",
    python_requires=">=3.6",
)
