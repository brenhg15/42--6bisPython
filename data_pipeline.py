#!/usr/bin/python3

import json
from data_stream import DataStream
from data_processor import NumericProcessor, TextProcessor, LogProcessor
from typing import Protocol, tuple, list


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [val for _, val in data]
        print("CSV Output:")
        print(", ".join(values))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        export_dict = {f"item_{rank}": val for rank, val in data}
        print("JSON Output:")
        print(json.dumps(export_dict))


class PipelineDataStream(DataStream):
    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            exported_items: list[tuple[int, str]] = []
            count = min(nb, len(proc._data_store))
            for _ in range(count):
                exported_items.append(proc.output())
            if exported_items:
                plugin.process_output(exported_items)


if __name__ == "__main__":
    print("=== Code Nexus Data Pipeline ===")
    stream = PipelineDataStream()

    print("Initialize Data Stream...")
    stream.print_processors_stats()

    num_proc = NumericProcessor()
    text_proc = TextProcessor()
    log_proc = LogProcessor()

    print("\nRegistering Processors")
    stream.register_processor(num_proc)
    stream.register_processor(text_proc)
    stream.register_processor(log_proc)

    batch1 = [
        "Hello world",
        [3.14, 1, 2.71],
        [
            {"log_level": "WARNING", "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO", "log_message": "User wil is connected"}
        ],
        42,
        ["Hi", "five"]
    ]

    print("Send first batch of data on stream:", batch1)
    stream.process_stream(batch1)
    stream.print_processors_stats()

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    stream.output_pipeline(3, csv_plugin)

    stream.print_processors_stats()

    batch2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {"log_level": "NOTICE", "log_message": "Certificate expires in 10 days"}
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]

    print("\nSend another batch of data:")
    stream.process_stream(batch2)
    stream.print_processors_stats()

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    stream.output_pipeline(5, json_plugin)

    stream.print_processors_stats()
