import csv
import sys
import os
from collections import Counter


def infer_type(values):
    """Infer basic data type of a column."""
    cleaned = [v for v in values if v.strip() != ""]

    if not cleaned:
        return "All Null"

    try:
        for v in cleaned:
            int(v)
        return "Integer"
    except:
        pass

    try:
        for v in cleaned:
            float(v)
        return "Float"
    except:
        pass

    return "String"


def summarize_csv(file_path):
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return

    if os.path.getsize(file_path) == 0:
        print("Error: CSV file is empty.")
        return

    try:
        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print("Error: No columns found.")
                return

            rows = list(reader)

            print("=" * 60)
            print("CSV SUMMARY REPORT")
            print("=" * 60)

            print(f"Total Rows    : {len(rows)}")
            print(f"Total Columns : {len(reader.fieldnames)}")
            print(f"Columns       : {', '.join(reader.fieldnames)}")

            report = []
            report.append("# CSV Summary Report\n")
            report.append(f"Total Rows: {len(rows)}")
            report.append(f"Total Columns: {len(reader.fieldnames)}\n")

            for col in reader.fieldnames:

                values = [row[col] if row[col] is not None else "" for row in rows]

                null_count = sum(
                    1 for v in values if v.strip() == ""
                )

                dtype = infer_type(values)

                counter = Counter(
                    v for v in values if v.strip() != ""
                )

                top5 = counter.most_common(5)

                print("\n--------------------------------------")
                print(f"Column : {col}")
                print(f"Type   : {dtype}")
                print(f"Blank Cells : {null_count}")

                report.append(f"## {col}")
                report.append(f"- Type: {dtype}")
                report.append(f"- Blank Cells: {null_count}")

                if top5:
                    print("Top 5 Values:")

                    report.append("- Top 5 Values:")

                    for value, count in top5:
                        print(f"   {value} -> {count}")

                        report.append(f"  - {value}: {count}")
                else:
                    print("All values are NULL.")

                    report.append("- All values are NULL.")

            with open("summary_report.md", "w", encoding="utf-8") as f:
                f.write("\n".join(report))

            print("\nReport exported as summary_report.md")

    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage:")
        print("python csv_summary.py sample.csv")
        sys.exit()

    summarize_csv(sys.argv[1])