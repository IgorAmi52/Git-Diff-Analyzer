from remote.github_api import GithubAPI
# More git remote providers can be added here(eg. GitLab, Bitbucket)


def get_remote_service(provider_name):
    """
    Return the appropriate remote service class based on the provider name.
    """
    if provider_name.lower() == 'github':
        return GithubAPI
    else:
        raise ValueError(f"Invalid Git remote provider: {provider_name}")
