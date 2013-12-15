from bs4 import BeautifulSoup
import sys

def main(argv):
    with open("/home/rup/ir/exp/param.i.I.test", "r") as f:
        l = f.readlines()
    prev = ""
    l_ = []
    n = 0
    for i in range(len(l)):
        l[i] = l[i].lstrip().rstrip()
        l[i] = l[i].lstrip("\n").rstrip("\n")
        l_.append(l[i])
        n = len(l_) - 1

        if i == 0:
            continue

        if l_[n].startswith("</"):
            if not l_[n-1].startswith("<"):
                e  = l_.pop()
                e1 = l_.pop()
                e2 = l_.pop()
                l_.append(e2 + e1 + e)
                n = len(l_) - 1
  
    for i in range(len(l_)):
        print l_[i]

if __name__ == "__main__":
    main(sys.argv[1:])

