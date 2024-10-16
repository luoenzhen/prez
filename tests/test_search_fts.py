from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from testcontainers.compose import DockerCompose

from prez.app import assemble_app
from prez.config import Settings


@pytest.fixture(scope="module", autouse=True)
def tc_compose(request: pytest.FixtureRequest):
    """Setup and Tear Down for Fuseki container"""
    try:
        filepath = Path(__file__).parent / "fuseki"
        compose = DockerCompose(filepath)
        compose.start()
    finally:
        request.addfinalizer(lambda: compose.stop())
    return compose


@pytest.fixture(scope="module")
def client(tc_compose: DockerCompose):
    port = tc_compose.get_service_port("fuseki")
    local_settings: Settings = Settings(
        _env_file=None,
        sparql_endpoint=f"http://localhost:{port}/ds",
        sparql_repo_type="remote",
    )
    app = assemble_app(local_settings=local_settings)
    return TestClient(app)


def test_fts_single_predicate(client: TestClient):
    """Test FTS with one search predicate.

    Test that search results are returned from a full text search
    query with just one search predicate.
    """

    # BUG: search endpoint not defined.
    #      something in the lifespan event not loading the profiles

    response = client.get("/search", params={"q": "sandgate"})
    assert response.status_code == 200
