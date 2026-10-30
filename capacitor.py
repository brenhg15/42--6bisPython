
from typing import cast
from ex3 import TransformCreatureFactory, TransformCapability


if __name__ == "__main__":
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()

    print("base:")
    base = factory.create_base()
    base_cap = cast(TransformCapability, base)
    print(base.describe())
    print(base.attack())
    print(base_cap.transform())
    print(base.attack())
    print(base_cap.revert())

    print("evolved:")
    evolved = factory.create_evolved()
    evolved_cap = cast(TransformCapability, evolved)
    print(evolved.describe())
    print(evolved.attack())
    print(evolved_cap.transform())
    print(evolved.attack())
    print(evolved_cap.revert())
