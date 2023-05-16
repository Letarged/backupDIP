def parse_output(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")
    data = data.split('\n')[1:]   
    return(data)