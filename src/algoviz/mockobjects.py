"Create some simple objects to test our UI"

import random
from custom_types import DataObject


def mock_list():
    return DataObject(
        name="TestList",
        category="list",
        visualized=False,
        data=[random.randint(0, 100) for _ in range(30)],
    )


def mock_cooridnate_grid():
    d = {}
    for _ in range(20):
        i = random.randint(0, 50)
        j = random.randint(0, 50)
        c = random.choice("#!./%")
        d[(i, j)] = c

    return DataObject(name="TestGrid", category="coord_dict", visualized=True, data=d)
