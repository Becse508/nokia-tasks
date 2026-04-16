from pathlib import Path
from json import dumps
from typing import Any

KEYS_WITH_ARRAY_TYPE = ["dns_servers"]

def parse_line(line: str) -> tuple[str, Any]:
    parts = line.split(":", 1)
    if (len(parts) != 2):
        return None, None
    
    # formazas
    key = parts[0].replace(".", "").strip().lower().replace(" ", "_")
    val = parts[1].strip()
    if key in KEYS_WITH_ARRAY_TYPE:
        val = [x.strip() for x in val.split(',')]
    
    return (key, val)

def parse(text: str) -> dict[str, Any]:
    result = []
    lines = text.split('\n')
    
    parsing = False
    for line in lines:
        if not parsing and "adapter" in line:
            parsing = True
            result.append({})
            
        elif line == "" or line.isspace():
            # ha most kezdodott a blokk akkor hagyja, ha nem akkor vege
            if parsing and len(result[-1]) != 0: 
                parsing = False
        
        elif parsing:
            key, val = parse_line(line)
            if key != None:
                result[-1][key] = val
            
    return result
        

def main():
    parsed_data = []
    for path in sorted(Path(".").glob("*.log")):
        parsed_data.append({
            "file_name": path.name,
            "adapters": parse(path.read_text())
        })
    
    print(dumps(parsed_data, indent=2))


if __name__ == "__main__":
    main()
