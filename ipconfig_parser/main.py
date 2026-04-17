from pathlib import Path
from json import dumps
from typing import Any
from sys import argv

ARG_UNIFORM = "uniform" in argv
ARG_FORCE = ("force" in argv) and ARG_UNIFORM

KEYS_WITH_ARRAY_TYPE = ["dns_servers"]
UNIFORM_KEYS = [
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


def make_uniform(data: list[dict], force: bool = False):
    for adapter in data:
        for key in UNIFORM_KEYS:
            if not key in adapter:
                adapter[key] = [] if key in KEYS_WITH_ARRAY_TYPE else ""
    
    if force:
        data[:] = [
            {
                k: v for k, v in adapter.items()
                if k in UNIFORM_KEYS
            }
            for adapter in data
        ]
    
    

# megnezem, hogy benne van-e az "adapter" szo a biztonsag kedveert
is_adapter_name = lambda line: "adapter" in line and line.endswith(':') and not line.startswith(" ")
is_end_of_block = lambda line: line == "" or line.isspace() or not line.startswith(" ")

# biztonsagos parse
def parse_safe(text: str, uniform: bool = False, force: bool = False) -> dict[str, Any]:
    result = []
    
    parsing = False
    just_started = False
    for line in text.split('\n'):
        # adapter nev = blokk kezdete
        if is_adapter_name(line):
            parsing = True
            just_started = True
            result.append({"adapter_name": line.strip()[:-1]})
        
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
    
    if uniform:
        make_uniform(result, force)
    return result


# kevesbe biztonsagos de szebb a kod (tokeletesen mukodik sima ipconfiggal)
def parse_short(text: str, uniform: bool = False, force: bool = False) -> dict[str, Any]:
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
    if uniform:
        make_uniform(result, force)
    return result

def main():
    parsed_data = []
    for path in Path(".").glob("*.log"):
        parsed_data.append({
            "file_name": path.name,
            "adapters": parse_safe(path.read_text(encoding='utf-8'), ARG_UNIFORM, ARG_FORCE)
        })
    
    print(dumps(parsed_data, indent=2))


if __name__ == "__main__":
    main()
