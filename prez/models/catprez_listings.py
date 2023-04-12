from typing import Optional, FrozenSet

from pydantic import BaseModel, root_validator
from rdflib import Namespace, URIRef
from rdflib.namespace import DCAT

PREZ = Namespace("https://prez.dev/")


class CatalogMembers(BaseModel):
    url_path: str
    uri: Optional[URIRef] = None
    general_class: Optional[URIRef]
    classes: Optional[FrozenSet[URIRef]]
    selected_class: Optional[URIRef] = None
    link_constructor: Optional[str]
    top_level_listing: Optional[bool] = True

    @root_validator
    def populate(cls, values):
        url_path = values.get("url_path")
        if url_path in ["/object", "/c/object"]:
            values["link_constructor"] = f"/c/object?uri="
        if url_path == "/c/catalogs":
            values["general_class"] = DCAT.Catalog
            values["link_constructor"] = "/c/catalogs"
            values["classes"] = frozenset([PREZ.CatalogList])
        return values
