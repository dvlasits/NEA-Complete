
#Start with no comments
NumComments = 0
#Loop through all the lines in the code
for line in script.splitlines():
    if "#" in line:
        #If line contains a # procced to check
        #if the # is not inside a quote
        OpenSingle = 0
        OpenDouble = 0
        Correct = 0
        #Loop through all charachters in line
        for char in line:
            #if you have single quotes and not within a double quotes
            #then toggle the single quote open variable
            if char == "'" and OpenDouble == 0:
                OpenSingle += 1
                OpenSingle %= 2
            #if you have double quotes and not within single quotes
            #then toggle the double quote open variable
            if char == '"' and OpenSingle == 0:
                OpenDouble += 1
                OpenDouble %= 2
            #If come accross a hasthag check both open variable
            #set to 0 and if so it is a comment
            if char == "#" and OpenDouble == 0 and OpenSingle == 0:
                Correct = 1
            #Whole line looped through as there could be a valid #
            #even if one of them wasn't valid
        #increment number of comments by one if Correct was set to one
        if Correct == 1:
            NumComments += 1
