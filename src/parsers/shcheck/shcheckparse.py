
import json
import src.parsers.shcheck.patterns as patterns

class shheaders:
    def __init__(self, address, result):
        self.address = address
        self.presentDict = result["present"] # detailed info 
        self.presentList = [] # just names of present headers
        for present_header in result["present"]:
            self.presentList.append(present_header)
        self.missing = result["missing"]
        self.numOfPresent = len(self.presentList)
        self.numOfMissing = len(self.missing)

    def __str__(self):
        return(
            "shcheck.py" + "\n\t" +
            "Address: " + str(self.address) + "\n\t" + 
            "Num of present headers: " + str(self.numOfPresent) + "\n\t" +
            "Num of missing headers: " + str(self.numOfMissing) + "\n\t" +
            "Present headers: " + str(self.presentList) + "\n\t" +
            "Missing headers: " + str(self.missing)
        )

# returns array of shheaders-class objects
# each reachable target is represented by 1 element in the array
def parse_output(output):
    data = ""
    for line in output.logs(stream=True):
        data += line.decode("utf-8")

    # print(data)
    jsonStr = json.loads(data)
    shchecked_targets = []
    for addr in jsonStr:
        next_reccord = shheaders(addr, jsonStr[addr])
        shchecked_targets.append(next_reccord)
    
    # [0] if shcheck.py is called againts 1 target at a time
    return (patterns.generate_output(shchecked_targets[0].missing, shchecked_targets[0].address))
  #  return shchecked_targets[0] 


    
    print(shchecked_targets[0].address)
    print()
    print(shchecked_targets[0].presentList)
    print()
    print(shchecked_targets[0].presentDict)
    print()
    print(shchecked_targets[0].missing[2])
    print()
    print(shchecked_targets[0].numOfPresent)
    print(shchecked_targets[0].numOfMissing)

