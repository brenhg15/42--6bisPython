#!/usr/bin/python3

from data_processor import DataProcessor, NumericProcessor
from data_processor import TextProcessor, LogProcessor
from typing import Any


class DataStream:
    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for element in stream:
            handled = False
            for proc in self.processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print(
                    "DataStream error Can't process element in stream: "
                    f"{element}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self.processors:
            print("No processor found, no data")
            return

        for proc in self.processors:
            name = proc.__class__.__name__.replace("Processor", " Processor")
            total = proc._total_processed
            remaining = len(proc._data_store)
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )


if __name__ == "__main__":
    print("=== Code Nexus Data Stream ===")
    stream_engine = DataStream()
    stream_engine.print_processors_stats()

    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()

    batch = [
        "Hello world",
        [3.14, 1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO",
             "log_message": "User wil is connected"}
        ],
        42,
        ["Hi", "five"]
    ]

    print("\nRegistering Numeric Processor")
    print(f"\nSend first batch of data stream: {batch}")
    stream_engine.register_processor(num_proc)
    stream_engine.process_stream(batch)
    stream_engine.print_processors_stats()

    print("\nRegistering other data processors")
    print("\nSend the batch again")
    stream_engine.register_processor(text_proc)
    stream_engine.register_processor(log_proc)
    stream_engine.process_stream(batch)
    stream_engine.print_processors_stats()

    print("\nConsume some elements from the data processors:"
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        num_proc.output()
    for _ in range(2):
        text_proc.output()
    for _ in range(1):
        log_proc.output()

    stream_engine.print_processors_stats()
