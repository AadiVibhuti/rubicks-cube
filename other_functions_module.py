def get_alpha(str1):
    str2=""
    for i in str1:
        if i in "abcdefghijklmnopqrstuvwxyz":
            str2+=i
    return(str2)
def mod(a,b):
    b= abs(b)
    if a>=0:
        return a%b
    else:
        return -(-a%b)
def get_key(value,dictionary):
    keys=[]
    for k,v in dictionary.items():
        if v==value:
            keys.append(k)
    return(keys)