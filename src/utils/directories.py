import os

def create_output_dirs():

    directories = [
        "outputs",
        "outputs/gantt",
        "outputs/logs",
        "outputs/metrics",
        "outputs/tables",
        "outputs/comparison"
    ]

    for directory in directories:

        os.makedirs(directory, exist_ok=True)