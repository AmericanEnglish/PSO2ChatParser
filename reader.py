from datetime import datetime
# strptime
# Given a file and search terms returns pass or failx
def search_file(current_file, parameters):
    """(filename, list of search parameters) -> list of line numbers
        
    Returns a list of lines which match the search criteria"""
    # Parameters
    # [DateTime, SID, PID, ChatType, Keywords]
    # Read in file
    with open(current_file, "r", encoding="utf16") as cur:
        allText = cur.read()
    # Split file
    split_file = allText.split("\n")
    count = 0
    line_numbers = []
    # Console.WriteLine(current_file);
    for line in split_file:
        # Increment line number
        count += 1
        # Split the line
        split_line = line.split("\t")

        # Possibly empty?
        if len(split_line) == 0: 
            # Console.WriteLine("Line {0}: Split line is empty? Skipping!", count);
            continue;
        # Too many tabs
        if len(split_line) > 6:
            # Console.WriteLine("\tLength > 6!");
            # Console.WriteLine(split_line);
            split_line = too_many_tabs(split_line)
        
        # Victim of a bad newline
        if len(split_line) < 6:
            # Need to find the line that fits!
            tracking_index = count - 1
            keep = [];
            while True:
                tracking_index -= 1
                keep = split_file[tracking_index].split("\t")
                if len(keep) == 6:
                    break
            #  } while (keep.Length < 6) ;
            # Console.WriteLine("\tKeeping:   {0}", String.Join(", ", keep));
            #  for (int i = tracking_index + 1; i <= count - 1; i++) {
            i = tracking_index + 1
            while i <= count - 1:
                keep[5] += "\n" + split_file[i]
                i += 1
            # Console.WriteLine("\tFinalized: {0}", String.Join(", ", keep));
            split_line = keep

        # Check length of the array first
        if len(split_line) == 6:
            # Next use datetime
            #Console.WriteLine("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-");
            if (full_check(parameters, split_line)):
                num = int(split_line[1])
                if num not in line_numbers:
                #  if (!line_numbers.Contains(num)) {
                    #  line_numbers.Add(num);
                    line_numbers.append(num)
                # Console.WriteLine("Line {0} -> Success", split_line[1]);
            else:
                # Console.WriteLine("Line {0} -> Failed", split_line[1]);
                pass
        
        else:
            # Console.WriteLine("++++It's broken Jim");
            # Console.WriteLine("File: {0} | Line: {1}", current_file, count);
            # print_array(split_line);
            print("ERROR: LINE 72")
    return line_numbers

###############################
#  Helper Functions           #
###############################
def date_check(conditions, to_check):
    """(list of dates, string date) ->  bool
        
    Takes condinitions and a string. Checks the string via the date conditions provided"""
    # Console.WriteLine("\tDT  Search Terms [{0}] -> {1}", String.Join(", ", conditions), to_check);
    time_format = "%Y-%m-%dT%H:%M:%S"
    dt_to_check = datetime.strptime(to_check, time_format)
    #  DateTime dt_to_check = Convert.ToDateTime(to_check);
    if len(conditions) == 2:
        if conditions[0] is not None:
            dt_before = datetime.strptime(conditions[0], time_format)
            if conditions[1] is not None:
                dt_after = datetime.strptime(conditions[1], time_format)
                return (dt_before <= dt_to_check) and (dt_to_check <= dt_after)
            return dt_before <= dt_to_check
        elif conditions[1] is not None:
            dt_after = datetime.strptime(conditions[1], time_format)
            return dt_to_check <= dt_after
        else:
            return True
    # Console.WriteLine("\t\tPass Automatic");
    return True

def sid_check(conditions, to_check):
    """(list of SID strings, some SID) -> bool
    
    Take a list of SIDs and checks if to_check is any of them."""
    # This is an absolute check meaning that "1010" will not match "10101010"
    # Console.WriteLine("\tSID Search Terms [{0}] -> {1}", String.Join(", ", conditions), to_check);

    # This && seems redundant?
    #  if (conditions.Length >= 1 && !IsEmpty(conditions)):
    # Add search by and filter by options
    if len(conditions[2]) >= 1:
        for item in conditions:
            if (item == to_check):
                # Console.WriteLine("\t\tPass 1");
                return True;
        # Console.WriteLine("\t\tFail");
        return False;
    # Console.WriteLine("\t\tPass 2");
    return True;

def pid_check(conditions, to_check):
    """(list of pids, string of pid to compare) -> bool
    
    Takes a list of pids and a relative marker. Returns True if a condition
    loosely matches the to_check term.
    conditions[0] => search by bool
    conditions[1] => filter by bool"""
    # This check is relative or absolute so "Sus" might match with "Susan"
    # Console.WriteLine("\tPID Search Terms [{0}] -> {1}", String.Join(", ", conditions), to_check);
    # First term is either relative or not relative
    if conditions[0]:
        terms = conditions[2]
        for item in terms:
            if item.lower() in to_check.lower():
                # Console.WriteLine("\t\tPass 1");
                return True;
        else:
            return False
    # else:
    #     # Absolute
    #     for item in terms:
    #         if item == to_check:
    #             # Console.WriteLine("\t\tPass 2");
    #             return True;
    # Console.WriteLine("\t\tFail");
    return True  # failed all checks

def chat_check(conditions, to_check):
    """(list of tuples, single chat type) ->  bool
    
    Checks to see if the to_check term if of the correct chat type. Correct
    chat types are determined by the list of tuples which look like:
        ("GUILD", True)
        ("PUBLIC", False)"""
    # Console.WriteLine("\tChat Search Terms [{0}] -> {1}", String.Join(", ", conditions), to_check);
    # Console.WriteLine("\t\tPass?: {0}", Array.Exists(conditions, element => element == to_check));
    # This should have a SOME or ALL feature meaning that it returns true if it finds ONE condition vs ALL of them
    #  return (Array.Exists(conditions, element => element == to_check) && conditions.Length != 0);# This checks for ANY terms
    for item in conditions:
        if to_check == item[0]:
            # The bool determines if the chat is allowed
            return item[1]

def keyword_check(conditions, to_check):
    """(list of terms, some sentence) -> bool
    
    Searches for keywords in the string to_check."""
    # Console.WriteLine("\tKey Search Terms [{0}] -> {1}", String.Join(", ", conditions), to_check);
    # Should add a check for if ALL terms are found as well
    if conditions[0] and len(conditions[1]) > 1:
        terms = conditions[1]
        # Returns true if any terms or found
        for item in terms:
            return (item in to_check and conditions[0]) or (item.lower() in to_check.lower() and not conditions[0])
        return False
    else:
        # No keywords provided
        return True
    

def full_check(parameters, split_line):
    """(list of lists of strings, string) -> bool"""
    #  print("{} Datetime: {}".format(split_line[1], date_check(parameters[0], split_line[0])))
    #  print("{} SID Check: {}".format(split_line[1], sid_check(parameters[1], split_line[3])))
    #  print("{} PID Check: {}".format(split_line[1], pid_check(parameters[2], split_line[4])))
    #  print("{} Chat Type Check: {}".format(split_line[1], chat_check(parameters[3], split_line[2])))
    #  print("{} Keyword Check:{}".format(split_line[1], keyword_check(parameters[4], split_line[5])))
    return (
        date_check(parameters[0], split_line[0]) and
        sid_check(parameters[1], split_line[3]) and
        pid_check(parameters[2], split_line[4]) and 
        chat_check(parameters[3], split_line[2]) and
        keyword_check(parameters[4], split_line[5]))

def too_many_tabs(line):
    fodder = line[6:]
    # Keep the  first five entries
    keep = line[:6]
    keep.append("\t".join(fodder))
    return keep

if __name__ == "__main__":
    parameters = [
                    [], # DateTime 
                    [], # SID
                    ["not relative", "Kazumiko"],  # PID
                    [("PUBLIC", True), ("PARTY", True), ("GUILD", True), ("REPLY", True)], # Chat Type
                    [] # Keyword
                ]
    from sys import argv
    from os import listdir
    from functools import partial
    from time import time
    from multiprocessing import Pool, freeze_support
    freeze_support()
    if len(argv) == 1:
        location = "../logs/"
    else:
        location = argv[1]
        if location[-1] != "/":
            location += "/"
    allFiles = listdir(location)
    allFiles2 = list(map(partial(lambda x, loc: loc + x, loc=location), allFiles))
    print("Total Logs: {}".format(len(allFiles)))
    for i in range(18):
        t1 = time()
        mypool = Pool(i + 2)
        mypool.map(partial(search_file, parameters=parameters), allFiles2)
        t2 = time()
        print("PAR Time: {:4.3f}s ({} procs)".format(t2-t1, i + 2))
    #  allFiles3 = list(map(partial(search_file, parameters=parameters), allFiles2))
    #  for index, item in enumerate(allFiles3):
        #  if item != []:
            #  print("{}: {}".format(allFiles[index], len(item)))
    
