import os
import re

chapter_titles = {
    "4": "The Abstraction: The Process",
    "5": "Interlude: Process API",
    "6": "Mechanism: Limited Direct Execution",
    "7": "Scheduling: Introduction",
    "8": "Scheduling: The Multi-Level Feedback Queue",
    "9": "Scheduling: Proportional Share",
    "10": "Multiprocessor Scheduling (Advanced)",
    "13": "The Abstraction: Address Spaces",
    "14": "Interlude: Memory API",
    "15": "Mechanism: Address Translation",
    "16": "Segmentation",
    "17": "Free-Space Management",
    "18": "Paging: Introduction",
    "19": "Paging: Faster Translations (TLBs)",
    "20": "Paging: Smaller Tables",
    "21": "Beyond Physical Memory: Mechanisms",
    "22": "Beyond Physical Memory: Policies",
    "26": "Concurrency: An Introduction",
    "27": "Interlude: Thread API",
    "28": "Locks",
    "29": "Locked Data Structures",
    "30": "Condition Variables",
    "31": "Semaphores",
    "32": "Common Concurrency Problems",
    "33": "Event-based Concurrency (Advanced)",
    "36": "I/O Devices",
    "37": "Hard Disk Drives",
    "38": "Redundant Disk Arrays (RAID)",
    "39": "Interlude: Files and Directories",
    "40": "File System Implementation",
    "41": "Locality and The Fast File System",
    "42": "Crash Consistency: FSCK and Journaling",
    "43": "Log-structured File System (LFS)",
    "44": "Flash-based SSDs",
    "45": "Data Integrity and Protection",
    "48": "Distributed Systems",
    "49": "Sun's Network File System (NFS)",
    "50": "The Andrew File System (AFS)",
    "13-14": "Address Spaces & Memory API",
    "48-50": "Distributed File Systems",
}

def get_type_for_chapter(ch):
    if ch in ["4", "13", "26", "39", "48"]:
        return "concept"
    if ch in ["7", "8", "9", "10", "17", "22"]:
        return "algorithm"
    if ch == "32":
        return "pattern"
    return "mechanism"

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    # Match frontmatter
    fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not fm_match:
        return

    fm = fm_match.group(1)
    
    # Update type
    current_type_match = re.search(r'^type:\s*(.*)$', fm, re.MULTILINE)
    if current_type_match:
        current_type = current_type_match.group(1).strip()
        if current_type in ["atomic", "architecture", "atomic-note"]:
            # Need to derive type from source
            source_match = re.search(r'^source:\s*OSTEP Ch\.\s*([\d-]+)', fm, re.MULTILINE)
            if source_match:
                ch = source_match.group(1)
                new_type = get_type_for_chapter(ch)
                fm = re.sub(r'^type:\s*.*$', f"type: {new_type}", fm, flags=re.MULTILINE)
            else:
                # Default to concept if no chapter found
                fm = re.sub(r'^type:\s*.*$', f"type: concept", fm, flags=re.MULTILINE)

    # Update source
    source_match = re.search(r'^source:\s*OSTEP Ch\.\s*([\d-]+)(?!:)', fm, re.MULTILINE)
    if source_match:
        ch = source_match.group(1)
        if ch in chapter_titles:
            full_source = f'source: "OSTEP Ch. {ch}: {chapter_titles[ch]}"'
            fm = re.sub(r'^source:\s*OSTEP Ch\.\s*[\d-]+.*$', full_source, fm, flags=re.MULTILINE)

    new_content = f"---\n{fm}\n---" + content[fm_match.end():]
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root_dir in ["Virtualization", "Concurrency", "Persistence"]:
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".md"):
                process_file(os.path.join(root, file))