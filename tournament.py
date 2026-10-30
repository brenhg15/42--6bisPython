from ex3 import FlameFactory, TransformCreatureFactory
from ex4 import NormalStrategy, AggressiveStrategy, InvalidCreatureError


def run_tournament(opponents):
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    for i in range(len(opponents)):
        for j in range(len(opponents)):
            if i == j:
                continue
            fac1, strat1 = opponents[i]
            fac2, strat2 = opponents[j]

            c1 = fac1.create_base()
            c2 = fac2.create_base()

            print("\n* Battle *")
            print(c1.describe())
            print("vs.")
            print(c2.describe())
            print("now fight!")

            try:
                strat1.act(c1)
                strat2.act(c2)
            except InvalidCreatureError as e:
                print(f"Battle error, aborting tournament: {e}")
                return


if __name__ == "__main__":
    print("Tournament 0 (basic)")
    opponents_0 = [
        (FlameFactory(), NormalStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy())
    ]
    # Representación visual aproximada del ejemplo
    print("[(Flameling+Normal), (Shiftling+Aggressive)]")
    run_tournament(opponents_0)

    print("\nTournament 1 (error)")
    opponents_1 = [
        (TransformCreatureFactory(), AggressiveStrategy()),
        (FlameFactory(), AggressiveStrategy())
    ]
    print("[(Shiftling+Aggressive), (Flameling+Aggressive)]")
    run_tournament(opponents_1)
