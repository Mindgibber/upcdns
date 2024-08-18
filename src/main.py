import env
import http.client
import cfapi
# import json


def get_ip(host: str) -> str | None:
    conn = http.client.HTTPSConnection(host)
    conn.request("GET", "/", headers={"Host": host})
    resp = conn.getresponse()
    if resp.status == http.HTTPStatus.OK:
        data = resp.read().decode("utf-8")
        return data

    return None


def main():
    env_vars = env.load_env()
    if not env_vars:
        print("No config found")
        return
    cf = cfapi.Cf(
        env_vars["CFHOST"],
        env_vars["CFKEY"],
        env_vars["ZONEID"],
        env_vars["EMAIL"],
        env_vars["SITES"],
    )
    records = cf.get_record_id()
    ip = get_ip(env_vars["IPHOST"])
    if ip:
        print(ip)
        if records:
            for record in records:
                if record.ip != ip:
                    _ = cf.update_dns_record(ip, record.id)
                    print(f"{record.name} was updated: {record.ip}")
                else:
                    print(f"{record.name} ip was already updated")


if __name__ == "__main__":
    main()
