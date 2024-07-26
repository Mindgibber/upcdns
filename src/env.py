def load_env(file: str = ".env") -> dict[str, str]:
    env_vars: dict[str, str] = {}
    try:
        with open(file) as f:
            for line in f:
                line = line.split("#")[0]

                if line:
                    key, value = line.strip().split("=")
                    if key == "APIKEY":
                        if "Bearer " in value:
                            pass
                        else:
                            value = "Bearer " + value
                    env_vars[key] = value

    except FileNotFoundError:
        pass
    return env_vars
