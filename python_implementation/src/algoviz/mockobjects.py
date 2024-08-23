"Create some simple objects to test our UI"

import random
import uuid
from custom_types import DataObject


def mock_ascii_text():
    text = """
            _   _      _ _        __        __         _     _ _ _
            | | | | ___| | | ___   \ \      / /__  _ __| | __| | |
            | |_| |/ _ \ | |/ _ \   \ \ /\ / / _ \| '__| |/ _` | |
            |  _  |  __/ | | (_) |   \ V  V / (_) | |  | | (_| |_|
            |_| |_|\___|_|_|\___/     \_/\_/ \___/|_|  |_|\__,_(_)
            """

    grid = {}
    for i, row in enumerate(text.splitlines()):
        for j, c in enumerate(row):
            if c == " ":
                continue
            grid[(j, i)] = c

    return DataObject(
        name=str(uuid.uuid4()), category="grid", visualized=True, data=grid
    )


def mock_list():
    return DataObject(
        name=str(uuid.uuid4()),
        category="list",
        visualized=False,
        data=[random.randint(0, 100) for _ in range(30)],
    )


def mock_cooridnate_grid():
    d = {}
    for _ in range(20):
        i = random.randint(0, 20)
        j = random.randint(0, 20)
        c = random.choice("#!./%")
        d[(i, j)] = c

    return DataObject(name=str(uuid.uuid4()), category="grid", visualized=True, data=d)
