

def sendToLogger(log_level, log):
    if (log_level == "error"):
        print('Error: ' + str(log))
    elif (log_level == "warn"):
        print('Warning: ' + str(log))
    elif (log_level == "debug"):
        print('Debug: ' + str(log))
    else:
        print(log)