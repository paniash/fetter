def read_csv(path):
    with open(path, 'r+') as file:
        results = []

        for line in file:
            line = line.rstrip('\n') # remove `\n` at the end of line
            items = line.split(',')
            results.append(list(items))

        # after for-loop
        return results
