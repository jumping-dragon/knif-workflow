import re

import iocextract


def extract_iocs(haystack: str, refang: bool = True, strip: bool = False):
    return {
        "url": list(iocextract.extract_urls(haystack, refang=refang, strip=strip)),
        "ip": list(iocextract.extract_ips(haystack, refang=refang)),
        "hash": list(iocextract.extract_hashes(haystack)),
        "yara_rule": list(iocextract.extract_yara_rules(haystack)),
        "cve_id": extract_cve_ids(haystack),
        "mitre_attack_technique_id": extract_mitre_attack_technique_ids(haystack),
    }


def extract_cve_ids(haystack: str):
    # CVE regular expression
    pattern = r"CVE-\d{4}-\d{4,7}"
    cves = re.findall(pattern, haystack)
    unique_cves = list(dict.fromkeys(cves))
    return unique_cves


def extract_mitre_attack_technique_ids(haystack: str):
    pattern = r"T1[0-9]{3}(?:\.[0-9]{3})?"
    tech_ids = re.findall(pattern, haystack)
    unique_tech_ids = list(dict.fromkeys(tech_ids))
    return unique_tech_ids
