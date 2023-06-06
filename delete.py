import os
import random
import argparse
import time
import logging
import schedule

parser = argparse.ArgumentParser(description="Stationary folders don't sit still. Files older than the set time will be deleted. If you never use it, did you really need it?")

parser.add_argument('directory', type=str, help="Path of the directory to age")
parser.add_argument('-s', '--seconds', type=int, help='Time length in seconds')
parser.add_argument('-d', '--days', type=int, help='Time length in days')
parser.add_argument('-w', '--weeks', type=int, help='Time length in weeks')

args = parser.parse_args()

seconds = args.seconds
days = args.days
weeks = args.weeks

total_seconds = 0
if seconds:
    total_seconds += seconds
if days:
    total_seconds += days * 24 * 60 * 60
if weeks:
    total_seconds += weeks * 7 * 24 * 60 * 60

if total_seconds == 0:
    total_seconds = 604800 # default to one week

directory = args.directory

# logging folder movement history
logging.basicConfig(filename='delete_file_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def delete_random_file():
    current_time = time.time()
    # Collect the files that have not been accessed in a week
    files_to_delete = []

    # Iterate over all files in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Get the access time of the file in seconds
            access_time = os.path.getatime(file_path)

            # Calculate the time difference in seconds
            time_difference = current_time - access_time
            
            # Check if the file has not been accessed in given time frame
            if time_difference > total_seconds:
                files_to_delete.append(file_path)

    # Check if any files were found that have not been accessed in a week
    if files_to_delete:
        # Select a random file to delete
        file_to_delete = random.choice(files_to_delete)

        # Delete the file
        os.remove(file_to_delete)
        log_message = f"File deleted: {file_to_delete}"
        logging.info(log_message)
    # else:
    #     print("No files found that have not been accessed in a week.")

# Schedule the script to run once every minute
schedule.every(1).seconds.do(delete_random_file)

# Keep the script running indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)