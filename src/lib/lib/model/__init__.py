from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class PageStatus(StrEnum):
    ready = "ready"
    crawling = "crawling"
    finished = "finished"
    failed = "failed"


class Page(BaseModel):
    id: int
    site: str
    url: str
    meta: dict
    # content: str | None = None
    status: PageStatus = PageStatus.ready
    updated_at: datetime | None = None


class IocType(StrEnum):
    url = "url"
    ip = "ip"
    hash = "hash"
    yara_rule = "yara_rule"
    cve_id = "cve_id"
    mitre_attack_technique_id = "mitre_attack_technique_id"


class Ioc(BaseModel):
    id: int
    type: IocType
    key: str


class Relation(BaseModel):
    id: int
    iocs_id: int
    pages_id: int
