def parse_output(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
    data = data.split('\n')[1:] # odseknutie vymaže prvý element v poli, čo je úvodný riadok nástroja cewl, ako keby heading    
    return(data)