from dataclasses import dataclass
import http.client
import json

# from typing import Any, TypeAlias
from typing import Any, TypeAlias

cftmsg: TypeAlias = list[dict[str, int | str] | None]


@dataclass
class CfRecord:
    id: str
    zone_id: str
    zone_name: str
    name: str
    type: str
    content: str
    proxiable: bool
    proxied: bool
    ttl: int
    meta: dict[str, Any]
    comment: str | None
    tags: list[str]
    created_on: str
    modified_on: str
    priority: int | None = None
    data: dict[str, Any] | None = None


cftresult: TypeAlias = list[CfRecord | None]


@dataclass
class CfResponse:
    success: bool
    errors: cftmsg
    messages: cftmsg
    result: cftresult
    result_info: dict[str, Any] | None = None


def CfDecoder(
    dct: dict[
        str,
        cftmsg | cftresult | bool | None | dict[str, int] | int | str | dict[str, Any],
    ],
) -> CfResponse | CfRecord | dict[str, Any]:
    if "result" in dct:
        err: cftmsg = []
        messages: cftmsg = []
        result: cftresult = []
        resultsinfo: None | dict[str, int] = None
        success: bool = False
        if isinstance(dct["errors"], list):
            err = dct["errors"]
        if isinstance(dct["messages"], list):
            messages = dct["messages"]
        if isinstance(dct["result"], list):
            result = dct["result"]
        if isinstance(dct["result_info"], dict):
            resultsinfo = dct["result_info"]
        if isinstance(dct["success"], bool):
            success = dct["success"]
        return CfResponse(
            success=success,
            errors=err,
            messages=messages,
            result=result,
            result_info=resultsinfo,
        )
    if "id" in dct:
        id: str = ""
        zone_id: str = ""
        zone_name: str = ""
        name: str = ""
        type: str = ""
        content: str = ""
        proxiable: bool = False
        proxied: bool = False
        ttl: int = 0
        meta: dict[str, Any] = {}
        comment: str | None = None
        tags: list[str] = []
        created_on: str = ""
        modified_on: str = ""
        priority: int | None = None
        data: dict[str, Any] | None = None

        if isinstance(dct["id"], str):
            id = dct["id"]
        if isinstance(dct["zone_id"], str):
            zone_id = dct["zone_id"]
        if isinstance(dct["zone_name"], str):
            zone_name = dct["zone_name"]
        if isinstance(dct["name"], str):
            name = dct["name"]
        if isinstance(dct["type"], str):
            type = dct["type"]
        if isinstance(dct["content"], str):
            content = dct["content"]
        if isinstance(dct["proxiable"], bool):
            proxiable = dct["proxiable"]
        if isinstance(dct["proxied"], bool):
            proxied = dct["proxied"]
        if isinstance(dct["ttl"], int):
            ttl = dct["ttl"]
        if isinstance(dct["meta"], dict):
            meta = dct["meta"]
        if isinstance(dct["comment"], str):
            comment = dct["comment"]
        if isinstance(dct["tags"], list) and all(
            isinstance(val, str) for val in dct["tags"]
        ):
            tags = dct["tags"]
        if isinstance(dct["created_on"], str):
            created_on = dct["created_on"]
        if isinstance(dct["modified_on"], str):
            modified_on = dct["modified_on"]
        if "priority" in dct and isinstance(dct["priority"], int):
            priority = dct["priority"]
        if "data" in dct and isinstance(dct["data"], dict):
            data = dct["data"]

        return CfRecord(
            id=id,
            zone_id=zone_id,
            zone_name=zone_name,
            name=name,
            type=type,
            content=content,
            proxiable=proxiable,
            proxied=proxied,
            ttl=ttl,
            meta=meta,
            comment=comment,
            tags=tags,
            created_on=created_on,
            modified_on=modified_on,
            priority=priority,
            data=data,
        )

    return dct


@dataclass
class siteret:
    name: str
    id: str
    ip: str


class Cf:
    def __init__(
        self, host: str, apikey: str, zoneid: str, email: str, sites: list[str]
    ) -> None:
        self.host = host
        self.apikey = apikey
        self.zoneid = zoneid
        self.email = email
        self.sites = sites

    def verify_token(self):
        conn = http.client.HTTPSConnection(self.host)
        conn.request(
            "GET",
            "/client/v4/user/tokens/verify",
            headers={"Host": self.host, "Authorization": self.apikey},
        )
        resp = conn.getresponse()
        if resp.status == http.HTTPStatus.OK:
            data = resp.read().decode("utf-8")
            return data
        return ""

    def get_dns_records(self) -> str | None:
        conn = http.client.HTTPSConnection(self.host)
        try:
            conn.request(
                "GET",
                f"/client/v4/zones/{self.zoneid}/dns_records",
                headers={
                    "Host": self.host,
                    "Authorization": self.apikey,
                    "X-Auth-Email": self.email,
                },
            )
        except:
            return None
        resp = conn.getresponse()
        data = resp.read().decode("utf-8")
        return data

    def update_dns_record(self, newip: str, recordid: str):
        conn = http.client.HTTPSConnection(self.host)
        body = json.dumps({"content": newip})
        conn.request(
            "PATCH",
            f"/client/v4/zones/{self.zoneid}/dns_records/{recordid}",
            body,
            headers={
                "Host": self.host,
                "Authorization": self.apikey,
                "X-Auth-Email": self.email,
            },
        )
        resp = conn.getresponse()
        data = resp.read().decode("utf-8")
        return data

    def get_record_id(self) -> list[siteret] | None:
        sites: list[siteret] = []
        data = self.get_dns_records()
        if data:
            results: CfResponse = json.loads(data, object_hook=CfDecoder)
            for result in results.result:
                if result is not None:
                    if result.type == "A" and result.name in self.sites:
                        sites.append(
                            siteret(
                                name=result.name,
                                id=result.zone_id,
                                ip=result.content,
                            )
                        )
            return sites
        return None
