#!/usr/bin/python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self) -> None:
        self._data_store: list[str] = []
        self._total_processed: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data_store:
            raise IndexError("No data remaining to output.")
        item = self._data_store.pop(0)
        rank = self._total_processed - len(self._data_store) - 1
        return rank, item


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list) and data:
            return all(
                isinstance(x, (int, float)) and not isinstance(x, bool)
                for x in data
            )
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._data_store.append(str(item))
                self._total_processed += 1
        else:
            self._data_store.append(str(data))
            self._total_processed += 1


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        if isinstance(data, list) and data:
            return all(isinstance(x, str) for x in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._data_store.append(item)
                self._total_processed += 1
        else:
            self._data_store.append(data)
            self._total_processed += 1


class LogProcessor(DataProcessor):
    def _is_valid_log(self, item: Any) -> bool:
        return (
            isinstance(item, dict)
            and "log_level" in item
            and "log_message" in item
            and isinstance(item["log_level"], str)
            and isinstance(item["log_message"], str)
        )

    def validate(self, data: Any) -> bool:
        if self._is_valid_log(data):
            return True
        if isinstance(data, list) and data:
            return all(self._is_valid_log(x) for x in data)
        return False

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        items = data if isinstance(data, list) else [data]
        for item in items:
            formatted = f"{item['log_level']}: {item['log_message']}"
            self._data_store.append(formatted)
            self._total_processed += 1


if __name__ == "__main__":
    print("=== Code Nexus Data Processor ===")
    
    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()

    print("\nTesting Numeric Processor...")
    print(f"Trying to validate input '42': {num_proc.validate(42)}")
    print(f"Trying to validate input 'Hello': {num_proc.validate('Hello')}")
    
    print("\nTest invalid ingestion of string 'foo' without prior validation:")
    try:
        num_proc.ingest("foo")  # type: ignore
    except ValueError as e:
        print(f"Got exception: {e}")

    num_proc.ingest([1, 2, 3, 4, 5])
    print("\nProcessing data: [1, 2, 3, 4, 5]")
    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = num_proc.output()
        print(f"Numeric value {rank}: {val}")

    print("\nTesting Text Processor...")
    print(f"Trying to validate input '42': {text_proc.validate(42)}")
    text_proc.ingest(["Hello", "Nexus", "World"])
    print("Processing data: ['Hello', 'Nexus', 'World']")
    print("Extracting 1 value...")
    rank, val = text_proc.output()
    print(f"Text value {rank}: {val}")

    print("\nTesting Log Processor...")
    print(f"Trying to validate input 'Hello': {log_proc.validate('Hello')}")
    logs = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"}
    ]
    log_proc.ingest(logs)
    print(f"Processing data: {logs}")
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log_proc.output()
        print(f"Log entry {rank}: {val}")
