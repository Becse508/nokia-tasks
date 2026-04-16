from pathlib import Path

def next_magic_num(n: int):
    return n
    


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    nums = [
        next_magic_num(int(line))
        for line in data.split('\n')
        if line.isdecimal()
    ]
    print(nums)


if __name__ == "__main__":
    main()
