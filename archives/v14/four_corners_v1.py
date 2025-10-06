from datetime import datetime
from dataclasses import dataclass
from typing import List, Tuple
import itertools
import os


script_folder = os.path.dirname(os.path.abspath(__file__))
date_stamp = datetime.now().strftime("%Y%m%d")
file_stamp = datetime.now().strftime("%H.%M.%S")

"""
Storage Benchmark Test Parameter Generator

Generates test parameters for storage benchmarks with consistent total data movement
across different thread counts, folder structures, and file distributions.
"""


@dataclass
class BenchmarkParams:
    """Storage benchmark test parameters"""
    total_data_mb: int
    data_per_thread_mb: int
    thread_count: int
    folder_count: int
    files_per_folder: int
    file_size_mb: float

    def __str__(self):
        return (f"{self.data_per_thread_mb}MB × {self.thread_count} threads = "
                f"{self.total_data_mb}MB total | "
                f"{self.folder_count} folders × {self.files_per_folder} files/folder × "
                f"{self.file_size_mb:.2f}MB/file")


def generate_thread_combinations(total_data_mb: int) -> List[Tuple[int, int]]:
    """Generate (data_per_thread, thread_count) combinations for given total data"""
    combinations = []

    # Find all divisors of total_data_mb for thread combinations
    for threads in range(1, total_data_mb + 1):
        if total_data_mb % threads == 0:
            data_per_thread = total_data_mb // threads
            combinations.append((data_per_thread, threads))

            # Stop when data_per_thread becomes too small to be practical
            if data_per_thread < 1:
                break

    return combinations


def generate_file_structure_combinations(total_data_mb: int) -> List[Tuple[int, int, float]]:
    """Generate (folder_count, files_per_folder, file_size_mb) combinations"""
    combinations = []

    # Common folder counts to test
    folder_counts = [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 50, 64, 100]

    for folders in folder_counts:
        # Find files_per_folder values that work well
        for files_per_folder in [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64, 100, 128]:
            total_files = folders * files_per_folder

            # Calculate file size needed
            if total_files > 0:
                file_size_mb = total_data_mb / total_files

                # Filter for practical file sizes (0.1MB to 1GB)
                if 0.1 <= file_size_mb <= 1024:
                    combinations.append((folders, files_per_folder, file_size_mb))

    return combinations


def generate_benchmark_parameters(total_data_sizes_mb: List[int]) -> List[BenchmarkParams]:
    """Generate comprehensive benchmark parameters for given data sizes"""
    all_params = []

    for total_data_mb in total_data_sizes_mb:
        print(f"\nGenerating parameters for {total_data_mb}MB total data:")
        print("=" * 60)

        # Get thread combinations
        thread_combos = generate_thread_combinations(total_data_mb)

        # Get file structure combinations
        file_structure_combos = generate_file_structure_combinations(total_data_mb)

        # Create all combinations
        for (data_per_thread, threads), (folders, files_per_folder, file_size) in itertools.product(
                thread_combos, file_structure_combos
        ):
            # Verify the math works out
            calculated_total = folders * files_per_folder * file_size
            if abs(calculated_total - total_data_mb) < 0.01:  # Allow small floating point errors
                params = BenchmarkParams(
                    total_data_mb=total_data_mb,
                    data_per_thread_mb=data_per_thread,
                    thread_count=threads,
                    folder_count=folders,
                    files_per_folder=files_per_folder,
                    file_size_mb=file_size
                )
                all_params.append(params)

        # Sort by thread count, then by folder count for better readability
        size_params = [p for p in all_params if p.total_data_mb == total_data_mb]
        size_params.sort(key=lambda x: (x.thread_count, x.folder_count, x.files_per_folder))

        # Print sample of parameters for this data size
        print(f"Generated {len(size_params)} parameter combinations")
        print("\nSample configurations:")
        for i, params in enumerate(size_params[:10]):  # Show first 10
            print(f"  {i+1:2d}. {params}")
        if len(size_params) > 10:
            print(f"  ... and {len(size_params) - 10} more configurations")

    return all_params


def filter_practical_parameters(params: List[BenchmarkParams]) -> List[BenchmarkParams]:
    """Filter parameters to remove impractical configurations"""
    filtered = []

    for p in params:
        # Skip configurations with too many threads (>64 is often impractical)
        if p.thread_count > 64:
            continue

        # Skip configurations with too many folders (>1000 folders might be excessive)
        if p.folder_count > 1000:
            continue

        # Skip configurations with too many files per folder (>10000 might be excessive)
        if p.files_per_folder > 10000:
            continue

        # Skip very small file sizes (< 0.5MB might not be representative)
        if p.file_size_mb < 0.5:
            continue

        filtered.append(p)

    return filtered


def export_to_csv(params: List[BenchmarkParams], filename: str = "benchmark_parameters.csv"):
    """Export parameters to CSV file"""
    import csv

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['total_data_mb', 'data_per_thread_mb', 'thread_count',
                      'folder_count', 'files_per_folder', 'file_size_mb']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for p in params:
            writer.writerow({
                'total_data_mb': p.total_data_mb,
                'data_per_thread_mb': p.data_per_thread_mb,
                'thread_count': p.thread_count,
                'folder_count': p.folder_count,
                'files_per_folder': p.files_per_folder,
                'file_size_mb': round(p.file_size_mb, 4)
            })

    print(f"\nExported {len(params)} parameter sets to {filename}")


def main():
    # Define total data sizes to test (in MB)
    data_sizes = [
        32,     # XX-Small: 32MB
        # 64,     # X-Small: 64MB
        # 128,    # Small: 128MB
        # 512,    # Medium: 512MB
        1024,   # Large: 1GB
        # 2048,   # X-Large: 2GB
        # 4096,   # XX-Large: 4GB
    ]

    print("====================================")
    print("Storage Benchmark Parameter Generator")
    print("====================================")

    # Generate all parameters
    all_params = generate_benchmark_parameters(data_sizes)

    # Filter to practical parameters
    practical_params = filter_practical_parameters(all_params)

    print(f"\nSummary:")
    print(f"Total parameter combinations: {len(all_params)}")
    print(f"Practical parameter combinations: {len(practical_params)}")

    # Export to CSV
    export_to_csv(practical_params)

    # Show some interesting examples
    print(f"\nInteresting parameter examples:")
    print("-" * 80)

    # Group by data size and show variety
    for size in data_sizes:
        size_params = [p for p in practical_params if p.total_data_mb == size]
        if size_params:
            print(f"\n{size}MB configurations:")
            # Show variety: min/max threads, min/max folders
            by_threads = sorted(size_params, key=lambda x: x.thread_count)
            by_folders = sorted(size_params, key=lambda x: x.folder_count)

            examples = [
                by_threads[0],  # Min threads
                by_threads[-1], # Max threads
                by_folders[0],  # Min folders
                by_folders[-1], # Max folders
            ]

            # Remove duplicates while preserving order
            seen = set()
            unique_examples = []
            for ex in examples:
                key = (ex.thread_count, ex.folder_count, ex.files_per_folder)
                if key not in seen:
                    seen.add(key)
                    unique_examples.append(ex)

            for ex in unique_examples:
                print(f"  {ex}")


if __name__ == "__main__":
    main()