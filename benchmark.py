"""Час повного пошуку, включно з підготовкою шаблону; читання файлів поза вимірами."""
import csv
from pathlib import Path
from statistics import median
import sys
from timeit import repeat

from search import boyer_moore, kmp, rabin_karp


def main():
    data = Path(__file__).resolve().parent / "data"
    writer = csv.writer(sys.stdout, lineterminator="\n")
    writer.writerow(["article", "case", "pattern", "characters", "index", "BM_ms", "KMP_ms", "RK_ms"])
    for name, encoding, present in [("article1.txt", "cp1251", "працює як лінійний пошук"),
                                     ("article2.txt", "utf-8-sig", "редагувати дані графу")]:
        text = (data / name).read_text(encoding=encoding)
        # Така сама довжина; останній символ відсутній у вихідних текстах.
        for label, pattern in [("present", present), ("absent", present[:-1]+"Ω")]:
            index = text.find(pattern)
            assert (index >= 0) == (label == "present")
            times = []
            for alg in (boyer_moore, kmp, rabin_karp):
                assert alg(text, pattern) == index
                times.append(median(repeat(lambda: alg(text, pattern), repeat=7, number=20))*1000/20)
            writer.writerow([name, label, pattern, len(text), index, *(f"{t:.6f}" for t in times)])


if __name__ == "__main__":
    main()
