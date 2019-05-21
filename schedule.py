#!/usr/bin/python3

import argparse

from core.parser import Parser
from core.output import ConstructXML
from core.exceptions.exceptions import InvalidInput, NotFound

def process_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="Brno hl.n.;Česko")
    parser.add_argument("--dest", default="Nové Zámky")
    args = parser.parse_args()
    return args.start, args.dest


def main():
    start, dest = process_args()
    parser = Parser(start, dest)
    
    try:
        routes = parser.get_routes()
    except InvalidInput as e:
        print(e)
        return 1
    except NotFound as e:
        print(e)
        return 1

    output = ConstructXML()
    output.print_xml(routes)


if __name__ == "__main__":
    main()
