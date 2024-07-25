import env
import http.client


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
    ip = get_ip(env_vars["IPHOST"])
    if ip:
        print(ip)


if __name__ == "__main__":
    main()
