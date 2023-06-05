# Idle Time

Things don't sit still when they're left alone. They gather dust, decay, change, or move around. Why would files be any different? 


**Shuffle** surfaces your long forgotten folders in new locations, moving them to new homes. 

**Delete** gets rid of files that are past the time period of necessity. If you haven't touched it in 10 years, did you really need it?


Made during the [The Boston Stupid Shit No One Needs & Terrible Ideas Hackathon](https://bostonstupidhackathon.com/). Not to actually be used. Instead
## *Use these scripts responsibly and at your own risk.*


Install the required dependencies using pip:
```
pip install -r requirements.txt
```

## Shuffle

Shuffle randomly rearranges folders within a specified directory after a certain time length of not being accessed. This ensures that your folders remain dynamic and never settle into monotony.

### Usage
To use the Shuffle script, follow these steps:

1. Run the script with the command:

```
python shuffle.py /path/to/directory -s <seconds> -d <days> -w <weeks>
```


2. Replace `/path/to/directory` with the path of the directory you want to shuffle.

3. Specify the desired time length using the following optional arguments:
- `-s` or `--seconds`: Time length in seconds
- `-d` or `--days`: Time length in days
- `-w` or `--weeks`: Time length in weeks

4. Confirm your intent to run the script when prompted.

## Delete

Randomly deletes files that haven't been accessed for a specified amount of time within a directory. If you don't miss it, you didn't need it.

### Usage

To use the Delete script, follow these steps:

1. Run the script with the command:

```
python delete.py /path/to/directory -s <seconds> -d <days> -w <weeks>
```


2. Replace `/path/to/directory` with the path of the directory you want to age.

3. Specify the desired time length using the following optional arguments:
- `-s` or `--seconds`: Time length in seconds
- `-d` or `--days`: Time length in days
- `-w` or `--weeks`: Time length in weeks

4. Confirm your intent to run the script when prompted.


