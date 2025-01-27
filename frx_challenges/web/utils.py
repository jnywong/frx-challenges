# From https://github.com/jupyter-server/jupyter_server/blob/fc0ac3236fdd92778ea765db6e8982212c8389ee/jupyter_server/config_manager.py#L14
def recursive_update(target: dict, new: dict) -> None:
    """
    Recursively update one dictionary in-place using another.

    None values will delete their keys.
    """
    for k, v in new.items():
        if isinstance(v, dict):
            if k not in target:
                target[k] = {}
            recursive_update(target[k], v)

        elif v is None:
            target.pop(k, None)

        else:
            target[k] = v