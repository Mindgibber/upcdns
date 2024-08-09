import http.client
import json


class Cf:
    def __init__(self, host: str, apikey: str, zoneid: str, email: str) -> None:
        self.host = host
        self.apikey = apikey
        self.zoneid = zoneid
        self.email = email

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

    def get_dns_records(self) -> str:
        conn = http.client.HTTPSConnection(self.host)
        conn.request(
            "GET",
            f"/client/v4/zones/{self.zoneid}/dns_records",
            headers={
                "Host": self.host,
                "Authorization": self.apikey,
                "X-Auth-Email": self.email,
            },
        )
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

    def get_record_id(self) -> str:
        data = self.get_dns_records()
        results = json.loads(data)
        for result in results["result"]:
            # print(result)
            if result["type"] == "A":
                print(result["name"])
                return result["id"]
        return ""
