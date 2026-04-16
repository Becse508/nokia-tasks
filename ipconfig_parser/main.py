from pathlib import Path
from json import dumps
from typing import Any

KEYS_WITH_ARRAY_TYPE = ["dns_servers"]
MUST_HAVE_KEYS = [
    "adapter_name",
    "description",
    "physical_address",
    "dhcp_enabled",
    "ipv4_address",
    "subnet_mask",
    "default_gateway",
    "dns_servers"
]


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

def handle_must_have_keys(data: list[dict]):
    for adapter in data:
        for key in MUST_HAVE_KEYS:
            if not key in adapter:
                adapter[key] = [] if key in KEYS_WITH_ARRAY_TYPE else ""

# megnezem, hogy benne van-e az "adapter" szo a biztonsag kedveert
is_adapter_name = lambda line: "adapter" in line and line.endswith(':') and not line.startswith(" ")
is_end_of_block = lambda line: line == "" or line.isspace() or not line.startswith(" ")

# biztonsagos parse
def parse_safe(text: str) -> dict[str, Any]:
    result = []
    
    parsing = False
    just_started = False
    for line in text.split('\n'):
        # adapter nev = blokk kezdete
        if is_adapter_name(line):
            parsing = True
            just_started = True
            result.append({"adapter_name": line[:-2].strip()})
        
        # blokk kozben
        elif (parsing and line.startswith(" ")):
            key, val = parse_line(line)
            if (key != None):
                result[-1][key] = val
        
        # blokk vege
        elif is_end_of_block(line):
            if just_started:
                just_started = False
            elif parsing:
                parsing = False
    
    handle_must_have_keys(result)
    return result


# kevesbe biztonsagos de szebb a kod (tokeletesen mukodik sima ipconfiggal)
def parse_short(text: str) -> dict[str, Any]:
    result = []
    
    for line in text.split('\n'):
        # adapter nev = blokk kezdete
        if (line.endswith(':') and not line.startswith(" ")):
            result.append({"adapter_name": line[:-2].strip()})
        
        # blokk kozben
        elif (line.startswith(" ")):
            key, val = parse_line(line)
            if (key != None):
                result[-1][key] = val
    
    handle_must_have_keys(result)
    return result

def main():
    parsed_data = []
    for path in Path(".").glob("*.log"):
        parsed_data.append({
            "file_name": path.name,
            "adapters": parse_short(path.read_text(encoding='utf-8'))
        })
    
    print(dumps(parsed_data, indent=2))


if __name__ == "__main__":
    main()
