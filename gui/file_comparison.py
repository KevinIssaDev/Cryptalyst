import json
import os

class FileComparison:
    """
    A class for comparing original and encrypted files to analyze ransomware encryption patterns.

    This class provides functionality to compare two files byte by byte, identifying
    ranges where the files differ, which are assumed to be encrypted portions.

    Attributes:
        original_file (str): Path to the original, unencrypted file.
        encrypted_file (str): Path to the potentially encrypted file.

    Methods:
        __init__(original_file, encrypted_file): Initialize the FileComparison object.
        merge_ranges(ranges): Merge overlapping or adjacent ranges.
        compare(progress_callback=None): Compare the files and return analysis results.
    """
    def __init__(self, original_file, encrypted_file):
        self.original_file = original_file
        self.encrypted_file = encrypted_file

    def merge_ranges(self, ranges):
        if not ranges:
            return []
        
        merged = []
        current_start, current_end = ranges[0]
        
        for start, end in ranges[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                merged.append((current_start, current_end))
                current_start, current_end = start, end
        
        merged.append((current_start, current_end))
        return merged

    def compare(self, progress_callback=None):
        try:
            with open(self.original_file, 'rb') as f1, open(self.encrypted_file, 'rb') as f2:
                original_size = os.path.getsize(self.original_file)
                if original_size < 1024:
                    size_str = f"{original_size} bytes"
                elif original_size < 1024 * 1024:
                    size_str = f"{original_size / 1024:.2f} KB"
                elif original_size < 1024 * 1024 * 1024:
                    size_str = f"{original_size / (1024 * 1024):.2f} MB"
                else:
                    size_str = f"{original_size / (1024 * 1024 * 1024):.2f} GB"
                encrypted_size = os.path.getsize(self.encrypted_file)

                if original_size != encrypted_size:
                    raise ValueError("Original and encrypted files have different sizes.")

                chunk_size = 1024 * 1024  # 1 MB chunks
                total_chunks = (original_size + chunk_size - 1) // chunk_size

                encrypted_ranges = []
                start = None
                processed_bytes = 0

                for chunk in range(total_chunks):
                    original_chunk = f1.read(chunk_size)
                    encrypted_chunk = f2.read(chunk_size)

                    for i, (b1, b2) in enumerate(zip(original_chunk, encrypted_chunk)):
                        if b1 != b2:
                            if start is None:
                                start = processed_bytes + i
                        elif start is not None:
                            encrypted_ranges.append((start, processed_bytes + i))
                            start = None

                    processed_bytes += len(original_chunk)
                    if progress_callback:
                        progress_callback(int(processed_bytes / original_size * 100))

                if start is not None:
                    encrypted_ranges.append((start, original_size))

            # Merge adjacent ranges
            merged_ranges = self.merge_ranges(encrypted_ranges)

            encrypted_bytes = sum(end - start for start, end in merged_ranges)
            percentage_encrypted = (encrypted_bytes / original_size) * 100

            report = {
                "original_file": self.original_file,
                "encrypted_file": self.encrypted_file,
                "total_size": original_size,
                "total_size_str": size_str,
                "percentage_encrypted": percentage_encrypted,
                "encrypted_ranges": merged_ranges
            }

            return report

        except Exception as e:
            raise Exception(f"Error during file comparison: {str(e)}")