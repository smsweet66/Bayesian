import sys
import re
from Bayesian import BayesianNetwork


def main():
    network = BayesianNetwork("A:B,C;B:C;C:D,E;D:E;E:F;F:G;G:")
    network.addProbability('A',
                           [["A:0", .72],
                            ["A:1", .28]])

    network.addProbability('B',
                           [["A", "A:0", "A:1"],
                            ["B:0", .35, .55],
                            ["B:1", .65, .45]])

    network.addProbability("C",
                           [["B", "B:0", "B:0", "B:1", "B:1"],
                            ["A", "A:0", "A:1", "A:0", "A:1"],
                            ["C:0", .79, .86, .35, .29],
                            ["C:1", .21, .14, .65, .71]])

    network.addProbability("D",
                           [["C", "C:0", "C:1"],
                            ["D:0", .3, .49],
                            ["D:1", .7, .51]])

    network.addProbability("E",
                           [["D", "D:0", "D:0", "D:1", "D:1"],
                            ["C", "C:0", "C:1", "C:0", "C:1"],
                            ["E:0", .09, .13, .29, .6],
                            ["E:1", .91, .87, .71, .4]])

    network.addProbability("F",
                           [["E", "E:0", "E:1"],
                            ["F:0", .08, .12],
                            ["F:1", .92, .88]])

    network.addProbability("G",
                           [["F", "F:0", "F:1"],
                            ["G:0", .36, .28],
                            ["G:1", .64, .72]])

    regex = "^(([A-G]=(T|F))(?:,([A-G]=(T|F)))*)$|(^$)"
    if len(sys.argv) != 2 or not bool(re.match(regex, sys.argv[1])):
        print(f"Number of arguments received: {len(sys.argv)}")
        print("Expected Format:")
        print(f"{sys.argv[0]} input")
        print("input must be a comma separated list of (node name)=(T/F)")
        print("example input")
        print("A=T,B=F,C=T")
        exit(1)

    print(f"query: {sys.argv[1]}\n{network.query(sys.argv[1])}")


if __name__ == '__main__':
    main()
