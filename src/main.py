import argparse
from copier import sync_directories

def main():
    parser = argparse.ArgumentParser(description="Sync files efficiently.")
    parser.add_argument("source", help="Source directory")
    parser.add_argument("destination", help="Destination directory")
    args = parser.parse_args()
    sync_directories(args.source, args.destination)

if __name__ == "__main__":
    main()
