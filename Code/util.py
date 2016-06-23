def factor(n):
    #returns a list of tuples containing factor pairs
    #e.g. factor(6) returns [(1,6), (2, 3)]
    res = [(1,n),(n,1)]
    for i in range(2,n):
        for j in range(2,n):
            if i*j == n:
                res.append((i,j))
    return res

