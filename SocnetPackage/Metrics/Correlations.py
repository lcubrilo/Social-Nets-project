# Linearity correlation
from logging import raiseExceptions

def pearsonCorrelation(x, y, cheat = None):
    if cheat == None: cheat = len(x) > 50
    # Helper function
    def getDeltas(x): x_avg = sum(x)/len(x); return [x_i - x_avg for x_i in x]
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

    # Remove -1, since it should never naturally occur
    for i, ey in enumerate(y):
        if ey == -1:
            x.pop(i); y.pop(i)

    x_deltas, y_deltas = getDeltas(x), getDeltas(y)

    numerator, denominator1, denominator2 = 0, 0, 0
    for dx, dy in zip(x_deltas, y_deltas):
        numerator += dx*dy
        denominator1 += dx**2; denominator2 += dy**2
    
    # Division by zero not allowed
    if denominator1 == 0 or denominator2 == 0: 
        return 0

    return numerator/(denominator1*denominator2)**0.5         

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

# Report correl data in a nice way
def correlData(x, y, ttl="-", showAmount=True, printReport=True, both = False):
    if len(x) != len(y):
        raise Exception("Must have equal length")
    import pandas as pd

    xName, yName = ttl.split("-")
    df = pd.DataFrame({xName:x, yName:y})
    #print(type(df), type(df.corr()[xName][yName]))
    #print("df x{}x \t corr x{}x".format(df, df.corr()))
    linearCorrelation = df.corr(method="pearson")[xName][yName]
    rankCorrelation = df.corr(method="spearman")[xName][yName]

    corrAmount = "\n(linear={:.2%} correlated={:.2%})\n".format(linearCorrelation, rankCorrelation)
    interpretation = correlMsg(linearCorrelation, "pearson") + " & " + correlMsg(rankCorrelation, "spearman") + " "

    
    if printReport and ttl != "-": 
        if abs(linearCorrelation) > 0.8 or abs(rankCorrelation) > 0.8: 
                print("    - " + ttl + ": " + interpretation + corrAmount[1:-1])
        return corrAmount
    
    if ttl != "-":
        #return corrAmount, linearCorrelation maybe this was better
        return corrAmount, max(abs(linearCorrelation), abs(rankCorrelation))
    
    #print("Correlations.py - I was supposed to return two numbers {}{} and reach this point.".format(linearCorrelation, anyCorrelation))
    #raise Exception("Returning da minimum. {}, {} => {}".format(linearCorrelation, anyCorrelation, min(linearCorrelation, anyCorrelation)))
    return linearCorrelation, rankCorrelation

def correlData2(x, y, context="-", showAmount=True, printReport=True):
    linearCorrelation, anyCorrelation = pearsonCorrelation(x, y), spearmanCorrelation(x, y)

    corrAmount = "\n(pearson={} spearman={})\n".format(round(linearCorrelation, 2), round(anyCorrelation, 2))
    interpretation = "Indicates " + correlMsg(linearCorrelation, "pearson") + " & " + correlMsg(anyCorrelation, "spearman") + " "
    
    retVal = corrAmount if showAmount else "\n" + interpretation + context

    thingsCorrelated = context.split("-")[1] if "-" in context else ""

    if printReport:
        if abs(linearCorrelation) > 0.3 or abs(anyCorrelation) > 0.3: 
            print("    - " + thingsCorrelated + ": " + interpretation[9:] + corrAmount[1:-1])
    
    if printReport: return retVal
    return retVal, linearCorrelation

# Helper function
def correlMsg(corrVal, corrNam):
        sign = " positive" if corrVal > 0 else " negative"
        shouldIPrintThisFinding = True
        if abs(corrVal) > 1:
            return "an error"
        elif abs(corrVal) > 0.8:
            strength = "a strong"
        elif abs(corrVal) > 0.5:
            strength = "some"
        else:
            shouldIPrintThisFinding = False
            strength = "no"
            sign = ""

        property = "linearity" if corrNam == "pearson" else "correlation"

        return "{}{} {}".format(strength, sign, property)
# Report distribution data in a nice way
def distReport(metricName, linearCorrelations, coals = ""):
    whatIsThis = "distribution"    
    # Determine chance to be exp and pow
    sa = ""; sb = ""
    if len(linearCorrelations) >= 4:
        expProb = abs(linearCorrelations[2]); powProb = abs(linearCorrelations[3])
        
        s1 = ""; s2 = ""
        if expProb > 1: s1 = "Error"
        elif expProb > 0.8: s1 =" probably is exponential {} ({:.2%}).".format(whatIsThis, expProb)

        if powProb > 1: s2 = "Error"
        elif powProb > 0.8: s2 =" probably is power {} ({:.2%}).".format(whatIsThis, powProb)

        # Conclude
        if s1 == "" or s2 == "": sa = s1+s2 # Just one is ok
        elif s1 == "error" or s2 == "error": sa = "error" # Error completely delegitimizes
        else: 
            sa = s1 if expProb > powProb else s2 # Take stronger one
            sa = "+{:.2%} {} likelier a".format(abs(expProb-powProb), coals) + sa[len(" probably is"):]

        # Still nothing? Damn.
        if sa == "": sa="very uninteresting, chances exp: {:.2%},  pow: {:.2%}.".format(expProb, powProb)

    elif len(linearCorrelations) >= 2:
        expProb = abs(linearCorrelations[0]); powProb = abs(linearCorrelations[1])
        s1 = ""; s2 = ""
        if expProb > 1: s1 = "Error"
        elif expProb > 0.8: s1 = "probably is exponential {} ({:.2%}).".format(whatIsThis, expProb)

        if powProb > 1: s2 = "Error"
        elif powProb > 0.8: s2 = "probably is power {} ({:.2%}).".format(whatIsThis, powProb)

        # Conclude
        if s1 == "" or s2 == "": sb = s1+s2 # Just one is ok
        elif s1 == "error" or s2 == "error": sb = "error" # Error completely delegitimizes
        else: 
            sb = s1 if expProb > powProb else s2 # Take stronger one
            sb = "+{:.2%} likelier a".format(abs(expProb-powProb)) + sb[len(" probably is"):]

        # Still nothing? Damn.
        if sb == "": sb="very uninteresting, chances exp: {:.2%},  pow: {:.2%}.".format(expProb, powProb)

    # Kakav je ovo raspad TODO    
    retVala = "    - " + metricName + "(coals): " + sa
    retValb = "    - " + metricName + "(noncoals): " + sb
    #print(retVal) 
    return retVala + "\n" + retValb

if __name__ == "__main__":
    x = [21, 92, 23, 17, 81, 48, 53, 46, 6, 93]
    y = [91, 50, 96, 90, 1, 63, 37, 59, 60, 77]

    print(correlData(x, y, "nista-bull"))