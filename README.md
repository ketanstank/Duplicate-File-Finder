# 🔍 Smart Duplicate File Finder

A simple but practical Python tool that scans a folder, detects duplicate files, and calculates how much storage space could potentially be recovered.

Instead of comparing filenames, the program uses **file size + SHA-256 hashing** to determine whether files contain exactly the same data.

## 🚀 Features

- 🔎 Recursively scans folders and subfolders
- ⚡ Uses file size as a fast first filter
- 🔐 Uses SHA-256 hashing to verify duplicates
- 📊 Groups duplicate files together
- 💾 Calculates potential storage savings
- 🛡️ Does not automatically delete files
- 🐍 Built entirely with Python's standard library

## 🧠 How It Works

The program uses a two-step process to make duplicate detection more efficient.

### Step 1 — Compare file sizes

Files with different sizes cannot be identical.

For example:

```text
photo1.jpg → 2.4 MB
photo2.jpg → 2.4 MB
document.pdf → 8.1 MB
