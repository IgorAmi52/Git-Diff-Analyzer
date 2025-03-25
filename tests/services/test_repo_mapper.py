import pytest
from git_diff_analyzer.remote.github_api import GithubAPI
from git_diff_analyzer.services.repo_mapper import get_remote_service


@pytest.mark.parametrize("provider_name", ['GitHub', 'github', 'GITHUB'])
def test_get_remote_service_valid(provider_name):
    """
    Test valid input for different
    capitalizations of 'github' as provider_name.
    """
    service_class = get_remote_service(provider_name)
    assert isinstance(service_class, type) and issubclass(
        service_class, GithubAPI), f"Expected GithubAPI class, but got {type(service_class)}"


@pytest.mark.parametrize("invalid_provider_name",
                         ['githab',
                          'invalid_input1',
                          'invalid_input2'])
def test_get_remote_service_invalid(invalid_provider_name):
    """
    Test invalid input for unsupported provider.
    """
    with pytest.raises(ValueError, match=f"Invalid Git remote provider: {invalid_provider_name}"):
        get_remote_service(invalid_provider_name)
