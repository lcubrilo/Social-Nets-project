def pearsonCorrelation(x, y):
    x_len = len(x); x_sum = sum(x); x_avg = x_sum/x_len
    y_len = len(y); y_sum = sum(y); y_avg = y_sum/y_len

    x_delta = [x_i - x_avg for x_i in x]
    y_delta = [y_i - y_avg for y_i in y]

    numerator, denominator1, denominator2 = 0, 0, 0
    for dx, dy in zip(x_delta, y_delta):
        numerator += dx*dy
        denominator1 += dx**2; denominator2 += dy**2
    
    return numerator/(denominator1*denominator2)         

def spearmanCorrelation(x, y):
    return pearsonCorrelation(valuesToRank(x), valuesToRank(y))

def valuesToRank(values):
    if len(list(values)) == len(set(values)):
        return values
    ranks = sorted(values)
    tmpSum = 0; length = 1
    
    for i in range(1, len(ranks)):
        if values[i] != values[i-1]:
            ranks[i-length:i] = [tmpSum/length]*length
            tmpSum = i; length = 1
        else:
            tmpSum += i; length +=1
    
    return ranks

def correlData(x, y):
    a, b = pearsonCorrelation(x, y), spearmanCorrelation(x, y)
    return " pearson={} spearman={}".format(round(a, 2), round(b, 2))