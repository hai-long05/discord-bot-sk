with open('data/pi', 'r') as file:
    line_count = 0
    for line in file:
        if line != 1:
            line_count += 1
            
        # with open('data/pi', 'w') as file:
        #     if line_count%52 == 0:
        #         file.write('\n')
        #     elif line_count%53 == 0:
        #         file.write('\n')


    print(line_count)