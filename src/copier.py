import os
import shutil
import time

def resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))

def copy_if_changed(src, dst, chunk_size=1024 * 1024):  # 1MB chunks
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied new file: {src} -> {dst}")
        return

    src_time = os.path.getmtime(src)
    dst_time = os.path.getmtime(dst)
    if src_time <= dst_time:
        print(f"No changes detected by timestamp")
        return

    src_size = os.path.getsize(src)
    dst_size = os.path.getsize(dst)
    changed = False

    with open(src, 'rb') as f_src, open(dst, 'r+b') as f_dst:
        offset = 0
        while True:
            src_chunk = f_src.read(chunk_size)
            dst_chunk = f_dst.read(chunk_size)

            if not src_chunk:
                break

            if src_chunk != dst_chunk:
                changed = True
                f_dst.seek(offset)
                f_dst.write(src_chunk)

            offset += len(src_chunk)

        remaining = f_src.read()
        if remaining:
            changed = True
            f_dst.seek(offset)
            f_dst.write(remaining)

    if src_size < dst_size:
        with open(dst, 'ab') as f_dst:
            f_dst.truncate(src_size)
            changed = True

    if changed:
        print(f"Updated file: {src} -> {dst}")
    else:
        print(f"No changes needed: {src} == {dst}")

def sync_directories(src_dir, dst_dir):
    src_dir = resolve_path(src_dir)
    dst_dir = resolve_path(dst_dir)

    for root, _, files in os.walk(src_dir):
        for filename in files:
            src_path = os.path.join(root, filename)
            rel_path = os.path.relpath(src_path, src_dir)
            dst_path = os.path.join(dst_dir, rel_path)
            start_time = time.time()
            copy_if_changed(src_path, dst_path)
            end_time = time.time()
            print(f"Time Taken: {end_time-start_time}")
