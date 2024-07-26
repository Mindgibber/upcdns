import env
import http.client
import json


def get_ip(host: str) -> str | None:
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", "/", headers={"Host": host})
    resp = conn.getresponse()
    if resp.status == http.HTTPStatus.OK:
        data = resp.read().decode("utf-8")
        return data

    return None


def verify_token(host: str, apikey: str):
    conn = http.client.HTTPSConnection(host)
    conn.request(
        "GET",
        "/client/v4/user/tokens/verify",
        headers={"Host": host, "Authorization": apikey},
    )
    resp = conn.getresponse()
    if resp.status == http.HTTPStatus.OK:
        data = resp.read().decode("utf-8")
        print(data)


def get_dns_records(host: str, apikey: str, zoneid: str) -> str:
    conn = http.client.HTTPSConnection(host)
    conn.request(
        "GET",
        f"/client/v4/zones/{zoneid}/dns_records",
        headers={"Host": host, "Authorization": apikey,
                 "X-Auth-Email": "wwd@sapo.pt"},
    )
    resp = conn.getresponse()
    data = resp.read().decode("utf-8")
    return data


def update_dns_record(host: str, apikey: str, zoneid: str, newip: str, recordid: str):
    conn = http.client.HTTPSConnection(host)
    body = json.dumps({"content": newip})
    conn.request(
        "PATCH",
        f"/client/v4/zones/{zoneid}/dns_records/{recordid}",
        body,
        headers={"Host": host, "Authorization": apikey,
                 "X-Auth-Email": "wwd@sapo.pt"},
    )
    resp = conn.getresponse()
    data = resp.read().decode("utf-8")
    print(data)


def main():
    env_vars = env.load_env()
    if not env_vars:
        print("No config found")
        return
    ip = get_ip(env_vars["IPHOST"])
    if ip:
        print(ip)


if __name__ == "__main__":
    main()
