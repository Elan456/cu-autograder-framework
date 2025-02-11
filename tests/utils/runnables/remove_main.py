import utils
import argparse


def main(target, output):
    utils.remove_main(target, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove main function from a file"
    )
    parser.add_argument(
        "target", help="Target C/C++ file to remove main function"
    )
    parser.add_argument("output", help="Output file to save the result")
    args = parser.parse_args()
    main(args.target, args.output)
