"""
AI Joi -- CLI entry point.
"""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="AI Joi")
    parser.add_argument("input", nargs="?", help="Input file or value")
    parser.add_argument("-o", "--output", help="Output file")
    args = parser.parse_args()

    print(f"AI Joi is running...")
    # TODO: implement your logic here

    return 0


if __name__ == "__main__":
    sys.exit(main())
