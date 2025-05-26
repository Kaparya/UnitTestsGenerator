import random


def generate_random_value(annotation: str):
    if annotation is None or annotation == "None":
        return None
    elif annotation == "int":
        return random.randint(0, 100)
    elif annotation == "float":
        return round(random.uniform(0.0, 100.0), 2)
    elif annotation == "str":
        return '"' + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5)) + '"'
    elif annotation == "bool":
        return random.choice([True, False])
    elif annotation.startswith("list") or annotation.startswith("List"):
        inside_value = generate_random_value(annotation[5:-1])
        return [inside_value for _ in range(3)]
    elif annotation.startswith("dict") or annotation.startswith("Dict"):
        return {str(i): random.randint(0, 10) for i in range(3)}
    elif annotation.startswith("Optional"):
        return random.choice([generate_random_value(annotation[9:-1]), None])
    return None
