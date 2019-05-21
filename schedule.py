#!/usr/bin/python3

import argparse

from parser import Parser
from output import ConstructXML


def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="Brno hl.n.;Česko")
    parser.add_argument("--dest", default="Nové Zámky")
    args = parser.parse_args()
    return args.start, args.dest


def main():
    start, dest = process_args()
    parser = Parser(start, dest)
    routes = parser.get_routes()
    output = ConstructXML()
    output.print_xml(routes)


if __name__ == "__main__":
    main()
