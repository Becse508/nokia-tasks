from pathlib import Path

# ez vegul nem kellett
def is_magic_num(n: int):
    num = str(n)
    return all([
        num[i] == num[-(i+1)]
        for i in range(len(num) // 2)
    ])

def next_magic_num(n: int) -> str:
    num = list(str(n)) # lista kell
    length = len(num)
    
    if (all([ch == "9" for ch in num])): # csak kilencesek
        return str(n+2)
    
    if (length == 1): # 1 szamjegy (nem 9)
        return str(n+1)
    
    for i in range(length // 2): # szimmetria kialakitasa
        num[-(i+1)] = num[i]
        
    
    num_str = "".join(num)
    idx = length // 2
    while int(num_str) <= n:
        if (num[idx] == '9'): # kijjebb lepunk
            num[idx] = '0'
            num[-(idx+1)] = '0'
            idx -= 1 # a csak 9-es mar az elejen elbukik, ugyhogy soha nem lesz minusz
        
        else: # noveljuk 1-el szimmetrikusan
            new_digit = str(int(num[idx])+1)
            num[idx] = new_digit
            num[-(idx+1)] = new_digit
            
        num_str = "".join(num)
    
    
    return num_str
    


def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    
    print("\n".join([
        f"next_magic_num({line}) => {next_magic_num(int(line))}"
        for line in data.splitlines()
        if line.isdecimal()
    ]))


if __name__ == "__main__":
    main()
