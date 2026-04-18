from pathlib import Path
from json import dumps
from typing import Any
from sys import argv

ARG_CLEAN = "clean" in argv                     # nem tart meg olyan beolvasott kulcsokat, aminek nincs erteke
ARG_UNIFORM = "uniform" in argv                 # minden adapterblokk tartalmazza a UNIFORM_KEYS kulcsokat is
ARG_FORCE = ("force" in argv) and ARG_UNIFORM   # minden adapterblokk csak a UNIFORM_KEYS kulcsokat tartalmazza

KEYS_WITH_ARRAY_TYPE = ["dns_servers", "default_gateway"]
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


def parse_line(line: str, prev_was_array: bool = False, clean: bool = False) -> tuple[bool, str, Any]:
    if (prev_was_array and line.startswith(("\t\t", " "*6))): # hozzaadjuk az elozo listahoz
        val = line.strip()
        return True, None, val if val != "" else None # ures erteket nem adunk vissza
    
    parts = line.split(":", 1)
    if (len(parts) != 2): # nem valid sor
        return False, None, None
    
    # formazas
    key = parts[0].replace(".", "").strip().lower().replace(" ", "_")
    val = parts[1].strip()
    
    if clean and val == "":
        return False, None, None
     
    if (key in KEYS_WITH_ARRAY_TYPE):
        val = [val.strip()]
        if (val[0] == ""): # nem akarunk [""] listat
            return False, key, []
    
    return False, key, val


def make_uniform(data: list[dict], force: bool = False):
    for adapter in data:
        for key in UNIFORM_KEYS:
            if not key in adapter:
                adapter[key] = [] if key in KEYS_WITH_ARRAY_TYPE else ""
    
    if force: # csak UNIFORM_KEYS kulcsok maradnak
        data[:] = [
            {
                k: v for k, v in adapter.items()
                if k in UNIFORM_KEYS
            }
            for adapter in data
        ]
    


is_adapter_name = lambda line: "adapter" in line and line.endswith(':') and not line.startswith(" ")
is_end_of_block = lambda line: line == "" or line.isspace() or not line.startswith(" ")

def parse(text: str, uniform: bool = False, force: bool = False, clean: bool = False) -> dict[str, Any]:
    result = []
    
    parsing = False
    prev_key = ""
    
    it = iter(text.splitlines())
    for line in it:
        # adapter nev = blokk kezdete
        if is_adapter_name(line):
            parsing = True
            result.append({"adapter_name": line.strip()[:-1]})
            next(it)
        
        # blokk kozben
        elif (parsing and line.startswith((" ", "\t"))):
            prev_was_array = isinstance(result[-1].get(prev_key), list)
            append, key, val = parse_line(line, prev_was_array, clean)
            
            if (append and val != None and prev_key != None):
                result[-1][prev_key].append(val)
            elif (key != None):
                result[-1][key] = val
                prev_key = key
            else:
                prev_key = None
        
        # blokk vege
        elif parsing and is_end_of_block(line):
            parsing = False
    
    if uniform:
        make_uniform(result, force)
    return result


def main():
    
    parsed_data = []
    for path in sorted(Path(".").glob("*.txt")):
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            text = path.read_text(encoding='utf-16')

        parsed_data.append({
            "file_name": path.name,
            "adapters": parse(text.strip(), ARG_UNIFORM, ARG_FORCE, ARG_CLEAN)
        })
    
    json_data = dumps(parsed_data, indent=2)
    print(json_data)
    Path("out.json").write_text(json_data, encoding="utf-8")


if __name__ == "__main__":
    main()
