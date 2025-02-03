from lib import generate_tests

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",
                        help="test",
                        action="store_true")

    args = parser.parse_args()
    generate_tests(args)


if __name__ == '__main__':
    main()
