def sortByPearsonOutliers(x, y):
    x_deltas, y_deltas = getDeltas(x), getDeltas(y)
    pearsonNumeratorTerms = [dx*dy for dx, dy in zip(x_deltas, y_deltas)]

    #also remove those that are zero, to avoid dividing by zero
    zipped = zip(x, y, pearsonNumeratorTerms)
    for (x, y, term) in zipped:
        if term == 0:
            zipped.remove((x, y, term))

    sorted_by_outlierness = sorted(zipped, key=lambda triple:triple[2], reverse=True)

    x = [triple[0] for triple in sorted_by_outlierness]
    y = [triple[1] for triple in sorted_by_outlierness]
    
    return x, y

def removePoutliers(x, y, p = 0.05):
    n = len(x)
    howManyToRemove = int(n*p)

    return sortByPearsonOutliers(x, y)[howManyToRemove:]

def getDeltas(x):
    x_len = len(x); x_sum = sum(x); x_avg = x_sum/x_len
    
    x_deltas = [x_i - x_avg for x_i in x]

    return x_deltas

def pearsonCorrelation(x, y, cheat = True):
    if cheat: x, y = removePoutliers(x, y)

    x_deltas, y_deltas = getDeltas(x), getDeltas(y)

    numerator, denominator1, denominator2 = 0, 0, 0
    for dx, dy in zip(x_deltas, y_deltas):
        numerator += dx*dy
        denominator1 += dx**2; denominator2 += dy**2
    
    if denominator1 == 0 or denominator2 == 0: return "error"

    return numerator/(denominator1*denominator2)         

def spearmanCorrelation(x, y):
    adjustedx, djustedy = valuesToRank(x), valuesToRank(y)
    return pearsonCorrelation(adjustedx, djustedy)

def valuesToRank(values):
    ranks = sorted(values)
    tmpSum = 0; length = 1
    
    for i in range(1, len(ranks)):
        if values[i] != values[i-1]:
            ranks[i-length:i] = [tmpSum/length]*length
            tmpSum = i; length = 1
        else:
            tmpSum += i; length +=1
    
    return ranks

def correlMsg(val, corr):
    sign = " positive" if val > 0 else " negative"

    if abs(val) > 1:
        return "an error"
    elif abs(val) > 0.5:
        strength = "a strong"
    elif abs(val) > 0.3:
        strength = "some"
    else:
        strength = "no"
        sign = ""

    property = "correlation" if corr == "pearson" else "linearity"

    return "{}{} {}".format(strength, sign, property)

def correlData(x, y):
    a, b = pearsonCorrelation(x, y), spearmanCorrelation(x, y)
    
    firstLine = "\n(pearson={} spearman={})\n".format(round(a, 2), round(b, 2))
    secondLine = "This indicates " + correlMsg(a, "pearson") + " & " + correlMsg(b, "spearman")
    return firstLine + secondLine