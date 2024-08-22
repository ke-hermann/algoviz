"Create some simple objects to test our UI"

import random
import uuid
from custom_types import DataObject


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
