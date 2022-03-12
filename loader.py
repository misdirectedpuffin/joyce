import csv

def main():
    with open(fname, mode='r') as f:
        headers = [
            "orig course",
            "course",
            "nat",
            "code",
            "course name",
            "forename",
            "surname",
            "class",
            "period",
            "aspirational target",
            "target",
            "working",
            "effort",
            "behaviour",
            "homework",
            "prelim",
            "baseline assessment",
            "sqa Prediction",
            "PASS N5",
            "PASS H"
        ]
        rows = csv.DictReader(f, fieldnames=headers)
        for r in rows:



if __name__ == '__main__':
    main()