# Cync

> A blazing-fast, I/O-efficient Python tool for local file synchronization.

**Cync** is a fast and efficient local file synchronization tool.  
It detects and syncs changes with minimal disk I/O, making updates faster and more resource-friendly.

---

## 🚀 Features

- **Metadata-based comparison**  
  Compares file size and modification timestamps before falling back to byte-level comparison.

- **Reduced disk I/O**  
  Skips files that haven't changed to avoid unnecessary reads/writes.

- **Partial file copying**  
  Only modified byte ranges are transferred, not entire files.

---

## 📦 Installation

You can install **Cync** via [PyPI](https://pypi.org/project/cync/) using pip:

```bash
pip install cync
```

Alternatively, clone the repository and run it directly:

```bash
git clone https://github.com/ZacharyShonk/Cync.git
cd Cync
python3 main.py /path/to/source /path/to/destination
```

---

## 🛠️ Usage

```bash
python3 -m cync /path/to/source /path/to/destination
```

or if running from the cloned repo:

```bash
python3 main.py /path/to/source /path/to/destination
```

- `/path/to/source`: The directory you want to sync from.
- `/path/to/destination`: The target directory to sync to.

---

## 👤 Author

- [@ZacharyShonk](https://github.com/ZacharyShonk)

---

## 📊 Project Status

[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Maintenance](https://img.shields.io/maintenance/yes/2025)](https://github.com/ZacharyShonk/Cync/projects)
[![Last Commit](https://img.shields.io/github/last-commit/ZacharyShonk/Cync)](https://github.com/ZacharyShonk/Cync/commits/main/)
[![Issues](https://img.shields.io/github/issues/ZacharyShonk/Cync)](https://github.com/ZacharyShonk/Cync/issues)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://github.com/ZacharyShonk/Cync/blob/main/LICENSE)

---

## 🔮 Planned Features (In order of priority)

- [ ] Add filters (includes/excludes)
- [ ] Dry-run mode to preview changes
- [ ] Progress bar with estimated time remaining
- [ ] Multithreaded syncing

---

## 📄 License

This project is licensed under the [GNU General Public License v3.0 (GPLv3)](https://choosealicense.com/licenses/gpl-3.0/).

You are free to use, modify, and distribute this software under the terms of this license.
