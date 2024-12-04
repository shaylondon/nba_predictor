from over_under import main as ou
from four_factors_moneyline import main as fourf

def main():
    open('../output.txt', 'w').close()
    ou()
    fourf()
    fourf()

if __name__ == "__main__": main()