from ex3 import TransformCreatureFactory


def test_capacitor():
    factory = TransformCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()

    for creature in [base, evolved]:
        print(creature.describe())
        print(creature.attack())
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


if __name__ == "__main__":
    print("Testing Creature with transform capability")
    print("base:")
    factory = TransformCreatureFactory()
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())

    print("evolved:")
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())
