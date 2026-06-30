#!/usr/bin/env python3
"""Find and extract the storage chip PDF."""
import os

inc = r'media/inbound'
for f in os.listdir(inc):
    sz = os.path.getsize(os.path.join(inc, f))
    # Print raw bytes to avoid encoding issues
    b = f.encode('utf-8', errors='replace')
    print(f'{sz:>10} | {b[:80]}')

print()
# The second PDF (largest but not 16MB)
for f in sorted(os.listdir(inc), key=lambda x: -os.path.getsize(os.path.join(inc, x))):
    sz = os.path.getsize(os.path.join(inc, f))
    if '.pdf' in f and sz < 14000000 and sz > 1000000:
        print(f'Likely storage chip PDF: {sz} bytes')
        src = os.path.join(inc, f)
        dst = r'C:\Users\Y\.openclaw\workspace\media\incoming\storage_chip_2026.pdf'
        import shutil
        shutil.copy2(src, dst)
        print(f'Copied to incoming')
        break
