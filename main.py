import sys
import os
import shutil
import time
import stat
import argparse
import logging

copied_inodes = {}

def folder_exists(path):
    """Returns the absolute file path if it exists, else None."""
    full_path = os.path.abspath(os.path.expanduser(path))
    if os.path.isdir(full_path):
        return full_path
    return None

def copy_symlink(src, dst):
    try:
        target = os.readlink(src)

        if os.path.islink(dst):
            existing = os.readlink(dst)
            if existing == target:
                return  # Skip recreating identical symlink

        if os.path.exists(dst) or os.path.islink(dst):
            os.remove(dst)

        os.symlink(target, dst)
        logging.info(f"Symlink copied: {src} -> {dst}")
    except Exception as e:
        logging.error(f"Failed to copy symlink: {src} -> {dst} ({e})")

def copy_changed_bytes(src_file, dst_file, block_size=4096):
    try:
        with open(src_file, 'rb') as src, open(dst_file, 'r+b') as dst:
            src_pos = 0
            while True:
                src_block = src.read(block_size)
                dst_block = dst.read(block_size)

                if not src_block and not dst_block:
                    break

                if src_block != dst_block:
                    dst.seek(src_pos)
                    dst.write(src_block)

                src_pos += len(src_block)

            src_size = src.tell()
            dst.seek(0, os.SEEK_END)
            dst_size = dst.tell()
            if dst_size > src_size:
                dst.truncate(src_size)

        shutil.copystat(src_file, dst_file)
        logging.info(f"Bytes updated: {src_file} -> {dst_file}")
    except PermissionError:
        logging.warning(f"Permission denied when copying: {src_file}")

def smart_copy_file(src_file, dst_file, block_size):
    try:
        st = os.lstat(src_file)
        key = (st.st_ino, st.st_dev)

        if os.path.islink(src_file):
            copy_symlink(src_file, dst_file)
        elif key in copied_inodes:
            if os.path.exists(dst_file):
                os.remove(dst_file)
            os.link(copied_inodes[key], dst_file)
            logging.info(f"Hard link created: {dst_file} -> {copied_inodes[key]}")
        elif not os.path.exists(dst_file):
            shutil.copy2(src_file, dst_file)
            copied_inodes[key] = dst_file
            logging.info(f"File copied: {src_file} -> {dst_file}")
        else:
            copy_changed_bytes(src_file, dst_file, block_size)
            copied_inodes[key] = dst_file
    except PermissionError:
        logging.warning(f"Permission denied: {src_file}")
    except Exception as e:
        logging.error(f"Failed to copy {src_file} -> {dst_file}: {e}")

def should_copy_file(src_file, dst_file, newer_only=False):
    try:
        src_stat = os.lstat(src_file)

        if sys.platform != "win32":
            mode = stat.S_IFMT(src_stat.st_mode)
            if mode in (stat.S_IFCHR, stat.S_IFBLK, stat.S_IFIFO, stat.S_IFSOCK):
                logging.info(f"Skipping special file: {src_file}")
                return False

        if not os.path.exists(dst_file):
            return True

        dst_stat = os.stat(dst_file)

        if src_stat.st_size != dst_stat.st_size:
            return True

        if src_stat.st_mtime != dst_stat.st_mtime:
            return src_stat.st_mtime > dst_stat.st_mtime if newer_only else True

        return False

    except PermissionError:
        logging.warning(f"Permission denied comparing: {src_file}")
        return False
    except FileNotFoundError:
        return True

def sync_folders(src, dst, newer_only, block_size, follow_symlinks):
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)

    if not os.path.exists(dst):
        os.makedirs(dst)

    for root, dirs, files in os.walk(src, topdown=True, followlinks=follow_symlinks):
        rel_path = os.path.relpath(root, src)
        dst_root = os.path.join(dst, rel_path)

        try:
            if os.path.islink(root) and not follow_symlinks:
                copy_symlink(root, dst_root)
                continue

            if not os.path.exists(dst_root):
                os.makedirs(dst_root)
        except PermissionError:
            logging.warning(f"Permission denied: {root}")
            continue

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_root, file)

            if os.path.islink(src_file) and not follow_symlinks:
                copy_symlink(src_file, dst_file)
            elif should_copy_file(src_file, dst_file, newer_only=newer_only):
                smart_copy_file(src_file, dst_file, block_size)

    for root, dirs, files in os.walk(dst, topdown=False):
        rel_path = os.path.relpath(root, dst)
        src_root = os.path.join(src, rel_path)

        for file in files:
            dst_file = os.path.join(root, file)
            src_file = os.path.join(src_root, file)
            try:
                if not os.path.lexists(src_file):
                    os.remove(dst_file)
                    if os.path.exists(dst_file):
                        logging.error(f"Failed to delete orphaned file: {dst_file}")
                    else:
                        logging.info(f"Removed orphaned file: {dst_file}")
            except PermissionError:
                logging.warning(f"Permission denied deleting: {dst_file}")

        for d in dirs:
            dst_dir = os.path.join(root, d)
            src_dir = os.path.join(src_root, d)
            try:
                if not os.path.exists(src_dir):
                    shutil.rmtree(dst_dir)
                    if os.path.exists(dst_dir):
                        logging.error(f"Failed to delete orphaned directory: {dst_dir}")
                    else:
                        logging.info(f"Removed orphaned directory: {dst_dir}")
            except PermissionError:
                logging.warning(f"Permission denied deleting dir: {dst_dir}")

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders efficiently.")
    parser.add_argument('--newer-only', action='store_true',
                        help='only copy files when source modification time is strictly newer than destination')
    parser.add_argument('--block-size', type=int, default=4096,
                        help='block size in bytes for byte-level difference copying')
    parser.add_argument('--follow-symlinks', action='store_true',
                        help='follow and recurse into symlinked directories and copy file targets instead of links')
    parser.add_argument('--log', action='store_true',
                        help='enable logging of sync actions')
    parser.add_argument('source', help='path to the source directory')
    parser.add_argument('destination', help='path to the destination directory')
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    source_folder = folder_exists(args.source)
    destination_folder = folder_exists(args.destination)

    if not source_folder:
        print("Source folder is not valid")
        sys.exit(1)
    if not destination_folder:
        print("Destination folder is not valid")
        sys.exit(1)

    print(f"Copying {source_folder} -> {destination_folder}...")
    start_time = time.time()
    sync_folders(source_folder, destination_folder,
                 newer_only=args.newer_only,
                 block_size=args.block_size,
                 follow_symlinks=args.follow_symlinks)
    end_time = time.time()
    print(f"Folder copied. Took {int(end_time - start_time)} seconds.")

if __name__ == "__main__":
    main()
