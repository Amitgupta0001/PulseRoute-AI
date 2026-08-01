import pandas as pd
from collections import Counter

from loader import DataLoader


class SampleAnalyzer:

    def __init__(self):

        self.loader = DataLoader().load()
        self.samples = self.loader.sample_messages

    def dataset_summary(self):

        print("=" * 60)
        print("SAMPLE DATASET SUMMARY")
        print("=" * 60)

        print(f"Rows    : {len(self.samples)}")
        print(f"Columns : {len(self.samples.columns)}")

        print("\nColumns")
        print(self.samples.columns.tolist())

    def action_distribution(self):

        print("\nAction Distribution")

        print(
            self.samples["action"]
            .value_counts(dropna=False)
        )

    def message_type_distribution(self):

        print("\nMessage Type Distribution")

        print(
            self.samples["message_type"]
            .value_counts(dropna=False)
        )

    def confidence_statistics(self):

        print("\nConfidence Statistics")

        print(
            self.samples["confidence"].describe()
        )

    def keyword_statistics(self, top_n=30):

        counter = Counter()

        for text in self.samples["reason"].fillna(""):

            for word in str(text).lower().split():

                word = word.strip(".,!?():;\"'")

                if len(word) < 3:
                    continue

                counter[word] += 1

        print("\nMost Common Reason Words\n")

        for word, freq in counter.most_common(top_n):

            print(f"{word:<20} {freq}")

    def routing_matrix(self):

        print("\nRouting Matrix\n")

        matrix = pd.crosstab(

            self.samples["message_type"],

            self.samples["action"]

        )

        print(matrix)

    def analyze(self):

        self.dataset_summary()

        self.action_distribution()

        self.message_type_distribution()

        self.confidence_statistics()

        self.keyword_statistics()

        self.routing_matrix()


def main():

    analyzer = SampleAnalyzer()

    analyzer.analyze()


if __name__ == "__main__":

    main()