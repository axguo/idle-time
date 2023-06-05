import os
import random
import argparse
import shutil
import time
import logging
import schedule

parser = argparse.ArgumentParser(description="Stationary folders don't sit still. Randomly rearrange your folders within a directory after a time length of not being accessed.")

parser.add_argument('directory', type=str, help="Path of the directory to shuffle")
parser.add_argument('-s', '--seconds', type=int, help='Time length in seconds')
parser.add_argument('-d', '--days', type=int, help='Time length in days')
parser.add_argument('-w', '--weeks', type=int, help='Time length in weeks')

args = parser.parse_args()

seconds = args.seconds
days = args.days
weeks = args.weeks

total_seconds = 604800 # default to one week
if seconds:
    total_seconds += seconds
if days:
    total_seconds += days * 24 * 60 * 60
if weeks:
    total_seconds += weeks * 7 * 24 * 60 * 60

directory = args.directory

# logging folder movement history
logging.basicConfig(filename='move_folder_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def get_random_destination_dir():
    # Get a list of all directories within the directory structure
    all_dirs = [
        os.path.join(root, dir)
        for root, dirs, files in os.walk(directory)
        for dir in dirs
    ]

    all_dirs.append(directory)

    # Select a random destination directory
    destination_dir = random.choice(all_dirs)

    return destination_dir

def is_subdirectory(path, directory):
    # Check if path is a subdirectory of directory
    path = os.path.normpath(path)
    directory = os.path.normpath(directory)

    return path.startswith(directory + os.path.sep)

def move_random_folder():
    current_time = time.time()
    # Collect the folders that have not been accessed in given time frame
    folders_to_move = []

    # Iterate over all folders in the directory
    for root, dirs, files in os.walk(directory):
        for dir in dirs:
            folder_path = os.path.join(root, dir)

            # Get the access time of the folder in seconds
            access_time = os.path.getatime(folder_path)

            # Calculate the time difference in seconds
            time_difference = current_time - access_time

            # Check if the folder has not been accessed in a week (7 days = 604800 seconds)
            if time_difference > total_seconds:
                folders_to_move.append(folder_path)

    # Check if any folders were found that have not been accessed in a week
    if folders_to_move:
        # Select a random folder to move
        folder_to_move = random.choice(folders_to_move)

        # Get the folder name
        folder_name = os.path.basename(folder_to_move)

        # Get the parent directory of the random folder
        parent_dir = os.path.dirname(folder_to_move)

        # Generate the destination directory path
        destination_dir = get_random_destination_dir()

        # Generate the destination path
        destination_path = os.path.join(destination_dir, folder_name)

        # Check if the destination path is a subdirectory of the original folder
        if not is_subdirectory(destination_path, folder_to_move):
            # Move the folder to the destination directory
            shutil.move(folder_to_move, destination_path)

            # Log the move information
            log_message = f"Moved: {folder_to_move} --> {destination_path}"
            logging.info(log_message)

    #     else:
    #         print("Inception. Skipping move operation.")
    # else:
    #     print("No folders found that have not been accessed recently. Good on you!")


# Display warning and ask for confirmation
print("****************************************")
print("*** WARNING: This script will shuffle ***")
print("*** the folders within the specified  ***")
print("*** directory based on the provided   ***")
print("*** time length. Make sure to backup  ***")
print("*** your data before running.         ***")
print("****************************************")
confirmation = input("Are you sure you want to run this script? (yes/no): ")

if confirmation.lower() == "yes":
    # Run the script once at the start
    move_random_folder()

    # Schedule the script to run once every minute
    schedule.every(1).seconds.do(move_random_folder)

    # Keep the script running indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    print("Script execution canceled.")