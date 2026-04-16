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
    if (key in KEYS_WITH_ARRAY_TYPE):
        val = [x.strip() for x in val.split(',')]
    
    return (key, val)

def parse(text: str) -> dict[str, Any]:
    result = []
    lines = text.split('\n')
    
    parsing = False
    just_started = False
    for line in lines:
        if ("adapter" in line and line.endswith(':') and not line.startswith(" ")):
            parsing = True
            just_started = True
            result.append({"adapter_name": line[:-2].strip()})
        
        elif (parsing and line.startswith(" ")):
            key, val = parse_line(line)
            if (key != None):
                result[-1][key] = val
        
        elif (line == "" or line.isspace() or not line.startswith(" ")):
            if just_started:
                just_started = False
            elif parsing:
                parsing = False
            
    return result
        

def main():
    parsed_data = []
    for path in sorted(Path(".").glob("*.log")):
        parsed_data.append({
            "file_name": path.name,
            "adapters": parse(path.read_text(encoding='utf-8'))
        })
    
    print(dumps(parsed_data, indent=2))


if __name__ == "__main__":
    main()
