import csv
import datetime

from blessed import Terminal

def choose_quote() -> str: 
    return "Those who do not get their hands dirty are wrong."

def get_time_remaining(end= datetime.datetime.now().replace(hour=16, minute=30, second=0, microsecond=0)):
    return str(end-datetime.datetime.now())[:-7]

def pretty_print_timedelta(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def main():
    start_time = datetime.datetime.now()

    # Set up Gui
    term = Terminal()

    print(term.home + term.clear + term.move_y((term.height // 2)-1))

    
    print(term.black_on_darkkhaki(term.center(choose_quote())))

    
    inp = None
    with term.cbreak(), term.hidden_cursor(), term.location(): 
        while term.inkey(timeout=0.02) != 'q':

            print(term.home())
            print(term.move_y(term.height//2))
            print(term.black_on_darkkhaki(term.center(f'Time remaining: {get_time_remaining()}')))



    end_time = datetime.datetime.now()
    time_worked = end_time-start_time
    print(term.move_down(2) + f'You worked for {pretty_print_timedelta(time_worked)}' )

    
    with open("/Users/Harry/org/caverns/data/deep_work.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([start_time, time_worked.total_seconds()])


    print(f'Saved to logs.' )
    


if __name__ == "__main__":
    main()

