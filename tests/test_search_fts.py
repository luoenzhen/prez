import pytest
# TODO: implement testcontainers
#       would be good to test FTS against an actual fuseki container.

@pytest.mark.skip(reason="Not Implemented")
def test_fts_single_predicate():
    """Test FTS with one search predicate.

    Test that search results are returned from a full text search
    query with just one search predicate.
    """
    # testing plan
    # - spin up fuseki with an in memory database Configured with a full text search index
    # - load pre-generated and indexed test data
    # - start prez
    # - make a search request to Prez
    # - confirm that results are returned
    # requirements
    # - pre-loaded (tdb2) and indexed test data
    pass
