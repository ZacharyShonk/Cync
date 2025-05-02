# 🚀 Cync

**Cync** is a high-speed folder synchronization tool designed to copy folders quickly and efficiently. It's lightweight, reliable, and ideal for frequent backups or folder mirroring tasks.

## ✅ Available Features

- Fast and efficient copying
- Preserves directory structure and file permissions
- One-way sync
- Smart updates (only copies changed files)
- Partial file updates (only changed byte ranges are written)
- Customizable filters (include/exclude files and folders)

## 🛠️ Planned Features (TODO)

- Dry-run mode to preview changes
- Optional checksum-based verification
- Multithreaded copying
- Python API for programmatic use
- Two-way sync
- File history
- Remote sync over network/SSH
- 7-Zip compression for transfer optimization

## ⚡ How It Achieves Fast Syncing

Cync is optimized for speed through several intelligent strategies:

- **File comparison by metadata**: Rather than comparing file contents byte-by-byte, Cync checks file size and modification timestamps to detect changes quickly.
- **Minimal disk I/O**: It avoids unnecessary disk access by skipping unchanged files entirely.
- **Incremental syncing**: Only new or modified files are transferred, reducing overall sync time.
- **Partial file updates**: When only part of a file has changed, Cync updates just the modified byte ranges—minimizing write operations and improving performance, especially on large files.
- **Planned: 7-Zip compression**: By compressing files before transfer using the efficient 7-Zip format, Cync will reduce I/O overhead and improve speed, particularly for syncing over slower drives or networks.
