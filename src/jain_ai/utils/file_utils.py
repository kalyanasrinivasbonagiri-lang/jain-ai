import os


def candidate_roots():
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    roots = []
    current = here

    for _ in range(5):
        roots.append(current)
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent

    roots.append(os.getcwd())
    return list(dict.fromkeys(roots))


def first_existing_path(*relative_paths):
    for root in candidate_roots():
        for relative_path in relative_paths:
            full_path = os.path.join(root, relative_path)
            if os.path.exists(full_path):
                return full_path
    return os.path.join(candidate_roots()[0], relative_paths[0])


def ensure_directories(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)


def load_local_env(env_path):
    if not os.path.exists(env_path):
        return

    try:
        with open(env_path, "r", encoding="utf-8") as file_obj:
            for raw_line in file_obj:
                line = raw_line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")

                if key and key not in os.environ:
                    os.environ[key] = value
    except OSError:
        pass
