from typing import TypedDict, cast


class Env(TypedDict):
    IPHOST: str
    CFHOST: str
    CFKEY: str
    ZONEID: str
    EMAIL: str
    SITES: list[str]


def load_env(file: str = ".env") -> Env:
    env_vars: dict[str, str | list[str]] = {}
    try:
        with open(file) as f:
            for line in f:
                line = line.split("#")[0]

                if line:
                    if "[" in line:
                        key, value = line.strip().split("=")
                        value = value.strip("[]")
                        value = value.replace('"', "")
                        value = value.replace("'", "")
                        env_vars[key] = value.split(",")
                    else:
                        key, value = line.strip().split("=")

                        if key == "APIKEY":
                            if "Bearer " in value:
                                pass
                            else:
                                value = "Bearer " + value
                        env_vars[key] = value

    except FileNotFoundError:
        pass
    return cast(Env, env_vars)
