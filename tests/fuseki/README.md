# Fuseki testing files

The files in this folder are used by testcontainers to spin up a Fuseki container for
testing the Fuseki full text search capabilities.

The `./test` folder contains a tdb2 database built with the tdb2.tdbloader command line
utility. It includes a Lucene Full-text index that was generated using the
`jena-fuseki-server-4.10.0.jar` jar according to the assembler description given in
`config.ttl`

The tdb database contains the data from `prez/test_data/vocprez.ttl`

**IMPORTANT**

As per the assembler description, The full text search is configured to index rdfs:label
and skos:prefLabel and to expose both of them under the propList with uri
prez:searchProps.

Thus we should expect results from all of the following

```sparql
select *
where {
    ?s text:query "demo"
}
```

```sparql
select *
where {
    ?s text:query ( rdfs:label "concept" )
}
```

```sparql
select *
where {
    ?s text:query ( prez:searchProps "concept" )
}
```
