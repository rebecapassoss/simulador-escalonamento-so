import json

def save_gantt(resultado, algoritmo):

    path = f"outputs/gantt/{algoritmo.lower()}_gantt.json"

    with open(path, "w") as f:

        json.dump(resultado, f, indent=4)