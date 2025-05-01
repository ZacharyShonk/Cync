import argparse
from copier import sync_directories

def main():
    parser = argparse.ArgumentParser(description="Sync files efficiently.")
    parser.add_argument("source", help="Source directory")
    parser.add_argument("destination", help="Destination directory")
    
    parser.add_argument(
        "-X", "--exclude",
        action="append", default=[],
        help="Glob pattern to exclude (applies to both files & dirs)"
    )
    parser.add_argument(
        "-I", "--include",
        action="append", default=[],
        help="Glob pattern to include (applies to both files & dirs)"
    )

    args = parser.parse_args()

    sync_directories(
        args.source,
        args.destination,
        exclude_patterns=args.exclude,
        include_patterns=args.include,
    )

if __name__ == "__main__":
    main()
