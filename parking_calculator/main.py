from pathlib import Path
from datetime import datetime, timedelta
from sys import argv

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
    
def calc_fine(time: timedelta, accurate: bool = False) -> float | int:
    hours = 0
    if (time.seconds != 0):
        if (accurate): # masodpercre pontos szamolas
            hours = time.seconds / HOURS
        else: # minden megkezdett ora
            hours = time.seconds // HOURS + 1
    
    # elso nap
    if (time.days == 0):
        # ingyenes 30 perc
        if (time.seconds <= 30 * MINUTES):
            return 0
        # olcso 3 ora
        if (hours <= 3):
            return hours * 300

        return 3 * 300 + (hours-3)*500
        
    
    return time.days * 10000 + hours * 500
    

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    accurate_fine = (len(argv) > 1 and argv[1] == "accurate")
    
    print("RENDSZAM      IDO                 AR\n"
          "================================================")
    for line in data.split('\n')[2:]:
        plate, start, end = parse(line)
        time = calc_time(start, end)
        fine = calc_fine(time, accurate_fine)
        
        print(f"{str(plate):<14}{str(time):<20}{str(int(fine)) + ' Ft':<10}")
    


if __name__ == "__main__":
    main()
