import json
import time
import datetime

def placeholder():
    return ""

a = open("access.log", "r")

t = time.time()
c = 0
hits = 0
miss = 0
bypass = 0
for x in a.readlines():
    p = json.loads(x[66:])
    try:
        ti = str(datetime.datetime.fromtimestamp(p["ts"]))
    except:
        ti = " "
    try:
        ip = p["request"]["headers"]["Cf-Connecting-Ip"][0] #X-Forwarded-For
    except:
        ip = p["request"]["remote_ip"]
    try:
        ua = p["request"]["headers"]["User-Agent"][0]
    except:
        ua = " - "
    print(str(ip) + " - - [" + ti + "] \"" + p["request"]["method"] + " " + p["request"]["uri"] +  " " + p["request"]["proto"] + "\" - " + str(p["status"]) + " " + str(p["size"]) + " - " + ua)
    c = c + 1

    #####################
    # Cache HIT/MISS Ratio
    #####################
    try:
        if p["resp_headers"]["Age"] != "0":
            hits = hits + 1
        else:
            miss = miss + 1
    except:
        bypass = bypass + 1


r = round(abs(t - time.time()), 3)
print("took " + str(r) + " seconds (" + str(round(c/r)) + " lines/second)")
print("Cache hit ratio: " + str((hits / (hits + miss)) * 100) + "% (" + str(bypass) + " cache bypasses)")
