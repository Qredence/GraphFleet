import numpy as np

def convert_numpy(obj):
    if isinstance(obj, np.generic):
        if isinstance(obj, np.bool_):
            return bool(obj)
        return obj.item()
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_numpy(value) for key, value in obj.items()}
    elif isinstance(obj, np.ndarray):
        return convert_numpy(obj.tolist())
    return obj