import numpy as np

def convert_numpy(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_numpy(value) for key, value in obj.items()}
    return obj