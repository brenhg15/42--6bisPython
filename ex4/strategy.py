#!/usr/bin/python3

from abc import ABC, abstractmethod
from typing import Any
from ex3 import TransformCapability


class InvalidCreatureError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, entity: Any) -> bool:
        pass

    @abstractmethod
    def act(self, entity: Any) -> None:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, entity: Any) -> bool:
        return True

    def act(self, entity: Any) -> None:
        print(entity.attack())


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, entity: Any) -> bool:
        return isinstance(entity, TransformCapability)

    def act(self, entity: Any) -> None:
        if not self.is_valid(entity):
            raise InvalidCreatureError(
                f"Invalid Creature '{entity.name}' "
                "for this aggressive strategy"
                )
        print(entity.transform())
        print(entity.attack())
        print(entity.revert())
