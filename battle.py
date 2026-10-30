#!/usr/bin/python3

from ex3 import FlameFactory, TransformCreatureFactory


def test_factory(factory):
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory1, factory2):
    c1 = factory1.create_base()
    c2 = factory2.create_base()
    print(c1.describe())
    print("vs.")
    print(c2.describe())
    print("fight!")
    print(c1.attack())
    print(c2.attack())


if __name__ == "__main__":
    print("Testing factory")
    f1 = FlameFactory()
    test_factory(f1)

    print("\nTesting factory")
    f2 = TransformCreatureFactory()
    test_factory(f2)

    print("\nTesting battle")
    test_battle(f1, f2)
