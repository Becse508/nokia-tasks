from pathlib import Path
from datetime import datetime, timedelta
from sys import argv
from math import ceil

HOURS = 3600
MINUTES = 60

def parse(text: str) -> tuple[str, datetime, datetime] | None:
    parts = text.split('		', 2)
    if (len(parts) < 3):
        return None
    
    return parts[0], datetime.fromisoformat(parts[1]), datetime.fromisoformat(parts[2])


def calc_time(start: datetime, end: datetime) -> timedelta:
    if (start > end):
        return timedelta(0)
    return end - start
    
def calc_fine(time: timedelta) -> float | int:
    minutes = 0
    if (time.seconds != 0):
        # percre pontos szamolas
        minutes = ceil(time.seconds / MINUTES)
    
    # egy nap
    if (time.days == 0):
        # ingyenes 30 perc
        if (minutes <= 30):
            return 0
        
        # olcso 3 ora - 30p
        if (minutes <= 3*60 + 30):
            return ceil((minutes - 30) / 60) * 300

        return min(3 * 300 + ceil((minutes - 3*60 - 30) / 60) * 500,
                   10000) # napi max
        
    # a feladat megfogalmazasa nem volt egyertelmu, gondolom igy kell tobb napot szamolni
    return time.days * 10000 + min(ceil(minutes / 60) * 500,
                                   10000) # napi max
    

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    
    # print("RENDSZAM      IDO                 AR\n"
    #       "================================================")
    for line in data.splitlines()[2:]:
        plate, start, end = parse(line)
        time = calc_time(start, end)
        fine = calc_fine(time)
        
        # print(f"{str(plate):<14}{str(time):<20}{str(int(fine)) + ' Ft':<10}")
        print(fine)
    


if __name__ == "__main__":
    main()
