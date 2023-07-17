from textwrap import dedent

from jinja2 import Template


def get_concept_scheme_query(iri: str, bnode_depth: int) -> str:
    query = Template(
        """
        PREFIX prez: <https://prez.dev/>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
        CONSTRUCT {  
            ?iri ?p ?o .
            
            {% if bnode_depth > 0 +%}
            ?iri ?p0 ?o0 .
            {% endif %}
            
            {% for i in range(bnode_depth) %}
            ?o{{ i }} ?p{{ i + 1 }} ?o{{ i + 1 }} .
            {% endfor %}
            
            ?iri prez:childrenCount ?childrenCount .
        }
        WHERE {
            BIND(<{{ iri }}> as ?iri)
            ?iri ?p ?o .
            FILTER (?p != skos:hasTopConcept)
            
            {
                SELECT (COUNT(?topConcept) AS ?childrenCount)
                WHERE {
                    BIND(<{{ iri }}> as ?iri)
                    ?iri skos:hasTopConcept ?topConcept .
                }
            }
            
            {% if bnode_depth > 0 %}
            ?iri ?p0 ?o0 .
            {% endif %}
            
            {% for i in range(bnode_depth) %}
            ?o{{ i }} ?p{{ i + 1 }} ?o{{ i + 1 }} .
            FILTER (isBlank(?o0))
            {% endfor %}
        }
    """
    ).render(iri=iri, bnode_depth=bnode_depth)

    return dedent(query)


def get_concept_scheme_top_concepts_query(iri: str, page: int, per_page: int) -> str:
    query = Template(
        """
        PREFIX prez: <https://prez.dev/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
        CONSTRUCT {
            ?concept skos:prefLabel ?label .
            ?concept prez:childrenCount ?narrowerChildrenCount .
            ?iri prez:childrenCount ?childrenCount .
            ?iri skos:hasTopConcept ?concept .
        }
        WHERE {
            BIND(<{{ iri }}> as ?iri)
            ?iri skos:hasTopConcept ?concept .
            ?concept skos:prefLabel ?label .
        
            {
                SELECT (COUNT(?childConcept) AS ?childrenCount)
                WHERE {
                    BIND(<{{ iri }}> as ?iri)
                    ?iri skos:hasTopConcept ?childConcept .
                }
            }
        
            {
                SELECT ?concept (COUNT(?narrowerConcept) AS ?narrowerChildrenCount)
                WHERE {
                    BIND(<{{ iri }}> as ?iri)
                    ?iri skos:hasTopConcept ?concept .
                    ?concept skos:prefLabel ?label .
                    
                    OPTIONAL {
                        ?narrowerConcept skos:broader ?concept .
                    }
                }
                GROUP BY ?concept
                ORDER BY ?label
                LIMIT {{ limit }}
                OFFSET {{ offset }}
            }
        }
    """
    ).render(iri=iri, limit=per_page, offset=(page - 1) * per_page)

    return dedent(query)


def get_concept_narrowers_query(iri: str, page: int, per_page: int) -> str:
    query = Template(
        """
        PREFIX prez: <https://prez.dev/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
        CONSTRUCT {
            ?concept skos:prefLabel ?label .
            ?iri prez:childrenCount ?childrenCount .
            ?iri skos:narrower ?concept .
        }
        WHERE {
            BIND(<{{ iri }}> as ?iri)
            ?concept skos:broader ?iri .
            ?concept skos:prefLabel ?label .
            
            {
                SELECT (COUNT(?childConcept) AS ?childrenCount)
                WHERE {
                    BIND(<{{ iri }}> as ?iri)
                    ?childConcept skos:broader ?iri .
                }
            }
        
            {
                SELECT ?concept ?label
                WHERE {
                    BIND(<{{ iri }}> as ?iri)
                    ?concept skos:broader ?iri .
                    ?concept skos:prefLabel ?label .
                }
                ORDER BY ?label
                LIMIT {{ limit }}
                OFFSET {{ offset }}
            }
        }
    """
    ).render(iri=iri, limit=per_page, offset=(page - 1) * per_page)

    return dedent(query)
