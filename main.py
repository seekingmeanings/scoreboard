from src.server import main as smain
import argparse as ap

if __name__ == "__main__":
    parser = ap.ArgumentParser()
    parser.add_argument("--verbosity", type=str, default="INFO")
    parser.add_argument("--virtual", action="store_true")
    args = parser.parse_args()

    smain(args)
