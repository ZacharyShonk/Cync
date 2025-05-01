import os
import shutil
import time
import fnmatch

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

def sync_directories(src_dir, dst_dir, exclude_patterns, include_patterns):
    src_dir = resolve_path(src_dir)
    dst_dir = resolve_path(dst_dir)

    for root, dirs, files in os.walk(src_dir):
        rel_root = os.path.relpath(root, src_dir)

        # Ignore excluded directorys
        kept = []
        for name in dirs:
            # includes
            if any(fnmatch.fnmatch(name, pat) for pat in include_patterns):
                kept.append(name)
            # excludes
            elif any(fnmatch.fnmatch(name, pat) for pat in exclude_patterns):
                print(f"Skipping directory {os.path.join(rel_root, name)}")
            else:
                kept.append(name)
        dirs[:] = kept

        for name in files:
            # includes
            if any(fnmatch.fnmatch(name, pat) for pat in include_patterns):
                copy = True
            # excludes
            elif any(fnmatch.fnmatch(name, pat) for pat in exclude_patterns):
                print(f"Skipping file {os.path.join(rel_root, name)}")
                copy = False
            else:
                copy = True

            if copy:
                src_path = os.path.join(root, name)
                rel_path = os.path.relpath(src_path, src_dir)
                dst_path = os.path.join(dst_dir, rel_path)
                start = time.time()
                copy_if_changed(src_path, dst_path)
                print(f"Time taken: {time.time() - start:.3f}s")
