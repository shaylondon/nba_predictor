from over_under import main as ou
from four_factors_moneyline import main as fourf

def main():
    open('../output.txt', 'w').close()
    fourf(5)
    ou()
    fourf(3)

if __name__ == "__main__": main()