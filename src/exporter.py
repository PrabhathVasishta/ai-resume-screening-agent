# src/exporter.py

import os
import json
import pandas as pd


class ResultExporter:
    """
    Exports screening results into CSV and JSON files.
    """

    def __init__(self, output_folder="output"):

        self.output_folder = output_folder

        os.makedirs(self.output_folder, exist_ok=True)

    def export_csv(
        self,
        results: list,
        filename="screening_results.csv"
    ) -> str:
        """
        Export results to CSV.
        """

        output_path = os.path.join(
            self.output_folder,
            filename
        )

        dataframe = pd.DataFrame(results)

        dataframe.to_csv(
            output_path,
            index=False,
            encoding="utf-8"
        )

        return output_path

    def export_json(
        self,
        results: list,
        filename="screening_results.json"
    ) -> str:
        """
        Export results to JSON.
        """

        output_path = os.path.join(
            self.output_folder,
            filename
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                results,
                file,
                indent=4,
                ensure_ascii=False
            )

        return output_path