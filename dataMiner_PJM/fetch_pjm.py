from get_subscription_headers import get_subsription_headers
from get_pjm_url import get_pjm_list, get_pjm_url
import requests, datetime, argparse, os, csv, io


VERSION = "1.0"
DEFAULT_OUTPUT_FORMAT = "csv"
NUMBER_OF_DAYS = 2000
ROW_COUNT = 100000
LAST_DAY = datetime.datetime(2024, 5, 1)

# Argument Parsing
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", "-u", help="URL key for data extraction. e.g., gen_by_fuel")
    parser.add_argument("--output", "-o", help="Set output filename")
    parser.add_argument("--list", "-l", help="Output list of all URLs", action="store_true")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    return parser.parse_args()
args = parse_arguments()

def get_header():
    headers = get_subsription_headers()
    print(f"Fetch subscription header {headers}")
    return headers

def output_data_list():
    list = get_pjm_list()
    print("|url|display name and description|")
    print("|---|---|")
    for l in list:
        print(f"|{l['name']}|*{l['displayName']}* {l['description']}|")

def parse_and_save_csv(content, filename):
    """Parse the CSV content and save it to a CSV file."""
    csv_reader = csv.reader(io.StringIO(content))
    file_exists = os.path.exists(filename)
    write_header = not file_exists or os.path.getsize(filename) == 0    
    with open(filename, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        print(f" Write Header? {write_header}")
        if write_header==False:
            header = next(csv_reader, None)
            if header:
                # csv_writer.writerow(header)
                pass
        
        for row in csv_reader:
            csv_writer.writerow(row)

def fetch_paginated_data(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(f"Response status code: {response.status_code}")
    # print(f"Response content: {response.text} Here it is.")
    content = response.content.decode('utf-8')
    if content.startswith('\ufeff'):
        content = content[1:]
    parse_and_save_csv(content, filename=args.output)
    return None

start_date = LAST_DAY - datetime.timedelta(days=NUMBER_OF_DAYS)
print(f"Start date: {start_date}")
def fetch_historical_data(url, headers):
    current_date = start_date
    while current_date <= LAST_DAY:
        print(f"Fetching data for {current_date}")
        formatted_date = current_date.strftime("%m-%d-%Y 00:00:00")
        formatted_date_end = current_date.strftime("%m-%d-%Y 23:59:59")
        historical_url = f"{url}?rowCount={ROW_COUNT}&startRow=1&datetime_beginning_ept={formatted_date} to {formatted_date_end}&format=csv"
        fetch_paginated_data(historical_url, headers) 
        current_date += datetime.timedelta(days=1)
    return None

def generate_output_filename(url, format):
    return f"{url}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{format}"

def save_data(data, output, format):
    data_to_write = data.export(format).strip('\n')
    with open(output, "w" if format != "xls" else "wb") as f:
        if format != "xls":
            f.write(data_to_write)
        else:
            f.write(data_to_write)


# Main Script Logic
if args.list:
    output_data_list()
    exit()

if not args.url:
    print("URL not provided")
    exit(1)

url = get_pjm_url(args.url)
print(f"Set URL to {url}")

headers = get_header()
fetch_historical_data(url, headers)
print("Complete")
