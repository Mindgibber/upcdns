def load_env(file: str = ".env") -> dict[str, str]:
    env_vars: dict[str, str] = {}
    try:
        with open(file) as f:
            for line in f:
                line = line.rstrip("#\n")

                if line:
                    key, value = line.strip().split("=")
                    env_vars[key] = value

    except FileNotFoundError:
        raise
    return env_vars
