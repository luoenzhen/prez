from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from rdflib.namespace import RDFS, SKOS
from testcontainers.compose import DockerCompose

from prez.app import assemble_app
from prez.config import Settings
from prez.enums import SearchMethod


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
    local_settings = Settings(
        _env_file=None,
        sparql_endpoint=f"http://localhost:{port}/testtdb",
        search_method=SearchMethod.fts_fuseki,
        search_predicates=[RDFS.label, SKOS.prefLabel],
    )
    app = assemble_app(local_settings=local_settings)
    with TestClient(app) as client:
        yield client


def test_fts_single_predicate(client: TestClient):
    """Test FTS with one search predicate.

    Test that search results are returned from a full text search
    query with just one search predicate.
    """

    response = client.get("/search", params={"q": "demo"})
    assert response.status_code == 200
