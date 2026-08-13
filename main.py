import hashlib
import os
from pathlib import Path
from collections import defaultdict

print("Starting duplicate file finder...")
def file_hash(filepath, chunk_size=1024 * 1024):
    """Return SHA-256 hash of a file without loading the whole file into memory."""
    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as file:
            while chunk := file.read(chunk_size):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (PermissionError, OSError):
        return None


def find_duplicates(folder):
    """Find duplicate files inside a folder and its subfolders."""

    folder = Path(folder)

    if not folder.exists():
        print("❌ Folder does not exist.")
        return {}

    if not folder.is_dir():
        print("❌ The path is not a folder.")
        return {}

    # Group files by size first.
    # Files with different sizes cannot be duplicates.
    files_by_size = defaultdict(list)

    print("\n🔍 Scanning files...\n")

    for root, _, files in os.walk(folder):
        for filename in files:
            filepath = Path(root) / filename

            try:
                size = filepath.stat().st_size
                files_by_size[size].append(filepath)
            except (PermissionError, OSError):
                continue

    # Only hash files where another file has the same size.
    duplicates = defaultdict(list)

    for size, files in files_by_size.items():

        if len(files) < 2:
            continue

        print(f"Checking {len(files)} files of size {format_size(size)}...")

        for filepath in files:
            file_hash_value = file_hash(filepath)

            if file_hash_value:
                duplicates[(size, file_hash_value)].append(filepath)

    # Remove groups containing only one file.
    return {
        key: files
        for key, files in duplicates.items()
        if len(files) > 1
    }


def format_size(size):
    """Convert bytes into a readable format."""

    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def main():
    print("=" * 60)
    print("        SMART DUPLICATE FILE FINDER")
    print("=" * 60)

    folder = input("\nEnter the folder to scan: ").strip()

    duplicates = find_duplicates(folder)

    if not duplicates:
        print("\n✅ No duplicate files found.")
        return

    wasted_space = 0
    duplicate_groups = 0

    print("\n" + "=" * 60)
    print("DUPLICATE FILES")
    print("=" * 60)

    for (size, _), files in duplicates.items():

        duplicate_groups += 1

        # Keep the first file and consider the rest unnecessary copies.
        wasted_space += size * (len(files) - 1)

        print(f"\n📁 Duplicate group ({format_size(size)} each):")

        for index, filepath in enumerate(files, start=1):
            print(f"   {index}. {filepath}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"Duplicate groups : {duplicate_groups}")
    print(f"Potential storage savings: {format_size(wasted_space)}")

    print("\n💡 No files were deleted.")
    print("Review the results and delete unwanted copies manually.")


if __name__ == "__main__":
    main()
