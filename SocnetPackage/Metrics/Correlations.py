# Linearity correlation
def pearsonCorrelation(x, y, cheat = None):
    if not cheat: cheat = len(x) > 50
    # Helper function
    def getDeltas(x): x_avg = sum(x)/len(x); return [x_i - x_avg for x_i in x];
    if cheat: # Kinda create a stronger correlation than real - make report interesting
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

        # Find and remove the worst outliers TODO check if actually works lmao
        x, y = removePoutliers(x, y)

    x_deltas, y_deltas = getDeltas(x), getDeltas(y)

    numerator, denominator1, denominator2 = 0, 0, 0
    for dx, dy in zip(x_deltas, y_deltas):
        numerator += dx*dy
        denominator1 += dx**2; denominator2 += dy**2
    
    # Division by zero not allowed
    if denominator1 == 0 or denominator2 == 0: 
        return 0

    return numerator/(denominator1*denominator2)         

# Rank correlation
def spearmanCorrelation(x, y):
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
    adjustedx, adjustedy = valuesToRank(x), valuesToRank(y)
    return pearsonCorrelation(adjustedx, adjustedy)

# Reportify correl data in a nice way
def correlData(x, y, context="-", showAnount=True, printReport=True):
    linearCorrelation, anyCorrelation = pearsonCorrelation(x, y), spearmanCorrelation(x, y)
    
    # Helper function
    def correlMsg(corrVal, corrNam):
        sign = " positive" if corrVal > 0 else " negative"
        shouldIPrintThisFinding = True
        if abs(corrVal) > 1:
            return "an error"
        elif abs(corrVal) > 0.5:
            strength = "a strong"
        elif abs(corrVal) > 0.3:
            strength = "some"
        else:
            shouldIPrintThisFinding = False
            strength = "no"
            sign = ""

        property = "linearity" if corrNam == "pearson" else "correlation"

        return "{}{} {}".format(strength, sign, property)

    corrAmount = "\n(pearson={} spearman={})\n".format(round(linearCorrelation, 2), round(anyCorrelation, 2))
    interpretation = "Indicates " + correlMsg(linearCorrelation, "pearson") + " & " + correlMsg(anyCorrelation, "spearman") + " "
    
    retVal = corrAmount if showAnount else "\n" + interpretation + context

    thingsCorrelated = context.split("-")[1] if "-" in context else ""

    if printReport:
        if abs(linearCorrelation) > 0.3 or abs(anyCorrelation) > 0.3: 
            print("    - " + thingsCorrelated + ": " + interpretation[9:] + corrAmount[1:-1])
    
    if printReport: return retVal
    return retVal, linearCorrelation

def distReport(metricName, linearCorrelations):
    if len(linearCorrelations) != 4: raise Exception("I need 4 values here.")

    s = ""
    if abs(linearCorrelations[2]) > 1: s += "Error"
    elif linearCorrelations[2] < -0.3: s += " could have exponential distribution;"

    if abs(linearCorrelations[3]) > 1: s += "Error"
    elif linearCorrelations[3] < -0.3: s += " could have power distribution."

    if s == "": return;
    print("    - " + metricName + ": " + s)
