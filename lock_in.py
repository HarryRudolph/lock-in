#!/usr/local/bin/python3
import argparse 
import csv
import datetime
import os
import random
import re 
import textwrap

from blessed import Terminal

def parse_arguments():
    parser = argparse.ArgumentParser(description="A script that takes debug mode and time as arguments.")
    
    # Add debug mode argument
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    
    # Add time argument
    parser.add_argument('-t', '--time', type=int, choices=range(1, 25), 
                        metavar="[1-24]", default=8,
                        help='Specify a time (integer between 1 and 24)')
    
    return parser.parse_args()


def choose_quote() -> str: 
    quotes_path = os.getenv("QUOTES_LOCATION") # Should be markdown backtick block quotes

    with open(quotes_path, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
        
        pattern = r'\`\`\`\n(.*?)\n\`\`\`'
        quotes_unclean = re.findall(pattern, markdown_content, re.MULTILINE | re.DOTALL)
        quotes = [quote.strip() for quote in quotes_unclean]

        return random.choice(quotes)
    return "Couldn't read quotes - lock_in.py"

def get_time_remaining():
    return end-datetime.datetime.now()

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
    args = parse_arguments()

    start_time = datetime.datetime.now()
    end = datetime.datetime.now().replace(hour=args.time, minute=0, second=0, microsecond=0)

    # Set up Gui
    term = Terminal()
    print(term.home + term.clear)

    # Calculate the position for the top third
    top_third_row = term.height // 3
    lines = textwrap.wrap(choose_quote(), term.width)
    vertical_offset = len(lines) // 2 

    # Print each line centered in the top third
    for i, line in enumerate(lines):
        with term.location(y=top_third_row - vertical_offset + i):
            print(term.center(line))

    #Time remaining
    print(term.move_y((term.height // 2)-1))
    time_remaining = datetime.timedelta(1000000)
    
    inp = None
    with term.cbreak(), term.hidden_cursor(), term.location(): 
        while term.inkey(timeout=0.02) != 'q':
            print(term.home())
            print(term.move_y(term.height//2))

            time_remaining = end - datetime.datetime.now()

            if time_remaining.total_seconds() < 0:
                print(term.black_on_red(term.center("your time is up, if only there was more.")))
                break
            
            print(term.black_on_darkkhaki(term.center(f'Time remaining: {str(time_remaining)[:-7]}')))

    end_time = datetime.datetime.now()
    time_worked = end_time-start_time
    print(term.move_down(2) + f'You worked for {pretty_print_timedelta(time_worked)}' )

    if not args.debug:
        with open("/Users/Harry/org/caverns/data/deep_work.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([start_time, time_worked.total_seconds()])

        print(f'Saved to logs.' )

if __name__ == "__main__":
    main()

