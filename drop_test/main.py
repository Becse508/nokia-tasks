from pathlib import Path
from math import comb

# milyen magassag lehetseges 'steps' lepessel
def calc_possible_height(pieces, steps): 
    return sum(comb(steps, n) for n in range(1, pieces+1))

def min_num_drops(pieces, height):
    for steps in range(1, height+1):
        possible_height = calc_possible_height(pieces, steps)
        if (possible_height >= height):
            return steps


def main():
    raw = Path("input.txt").read_text(encoding="utf-8")
    data = [line.split(", ") for line in raw.splitlines()]
    print("\n".join(
        f"min_num_drops({pieces}, {height}) => {min_num_drops(int(pieces), int(height))}"
        for pieces, height in data
    ))


if __name__ == "__main__":
    main()
