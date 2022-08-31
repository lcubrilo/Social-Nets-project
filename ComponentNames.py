def iterateThruComponentNames(name):
    def incChar(char):
        num = ord(char) - ord("A") + 1
        return chr(num % 26 + ord("A"))
    counter = 0
    res = ""
    while True:
        counter -= 1
        char = name[counter]
        res = incChar(char) + res
        if res[0] != "A":
            name = name[:counter] + res; return name
        if counter == -len(name):
            name = "A" + res; return name