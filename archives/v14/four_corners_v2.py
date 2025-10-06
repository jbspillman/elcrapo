"""
Storage Benchmark Test Parameter Generator with Multi-Host Support

Generates test parameters for storage benchmarks with consistent total data movement
across different thread counts, host counts, folder structures, and file distributions.
Tests can run from multiple hosts writing to the same shared directory.
"""

from dataclasses import dataclass
from typing import List, Tuple
import itertools


@dataclass
class BenchmarkParams:
    """Storage benchmark test parameters"""
    total_data_mb: int
    data_per_host_mb: int
    host_count: int
    threads_per_host: int
    data_per_thread_mb: int
    folder_count: int
    files_per_folder: int
    file_size_mb: float
    host_folder_strategy: str  # 'shared', 'dedicated', or 'mixed'

    @property
    def total_threads(self) -> int:
        return self.host_count * self.threads_per_host

    @property
    def total_files(self) -> int:
        return self.folder_count * self.files_per_folder

    def __str__(self):
        strategy_desc = {
            'shared': 'all hosts → same folders',
            'dedicated': 'each host → own folders',
            'mixed': 'hosts → mixed folder access'
        }

        return (f"{self.data_per_host_mb}MB × {self.host_count} hosts × "
                f"{self.threads_per_host} threads/host = {self.total_data_mb}MB total | "
                f"{self.folder_count} folders × {self.files_per_folder} files/folder × "
                f"{self.file_size_mb:.2f}MB/file | "
                f"{strategy_desc.get(self.host_folder_strategy, self.host_folder_strategy)}")


def generate_host_thread_combinations(total_data_mb: int) -> List[Tuple[int, int, int, int]]:
    """Generate (data_per_host, host_count, threads_per_host, data_per_thread) combinations"""
    combinations = []

    # Common host counts to test
    host_counts = [1, 2, 4, 8, 16, 32]

    for hosts in host_counts:
        if total_data_mb % hosts == 0:
            data_per_host = total_data_mb // hosts

            # Generate thread combinations per host
            for threads_per_host in range(1, min(65, data_per_host + 1)):  # Max 64 threads per host
                if data_per_host % threads_per_host == 0:
                    data_per_thread = data_per_host // threads_per_host

                    # Skip if data per thread becomes too small
                    if data_per_thread < 1:
                        break

                    combinations.append((data_per_host, hosts, threads_per_host, data_per_thread))

    return combinations


def generate_file_structure_combinations(total_data_mb: int, host_count: int) -> List[Tuple[int, int, float, str]]:
    """Generate (folder_count, files_per_folder, file_size_mb, strategy) combinations"""
    combinations = []

    # Base folder counts to test
    base_folder_counts = [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 50, 64, 100, 128, 256]

    # Folder access strategies
    strategies = ['shared', 'dedicated', 'mixed']

    for strategy in strategies:
        if strategy == 'dedicated':
            # Each host gets its own folders
            for base_folders in base_folder_counts:
                folder_count = base_folders * host_count  # Scale folders by host count

                # Generate file combinations
                for files_per_folder in [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64, 100, 128, 256]:
                    total_files = folder_count * files_per_folder

                    if total_files > 0:
                        file_size_mb = total_data_mb / total_files

                        # Filter for practical file sizes
                        if 0.1 <= file_size_mb <= 1024:
                            combinations.append((folder_count, files_per_folder, file_size_mb, strategy))

        else:  # 'shared' or 'mixed' strategies
            # All hosts share the same folder structure
            for folder_count in base_folder_counts:
                for files_per_folder in [1, 2, 4, 5, 8, 10, 16, 20, 25, 32, 40, 50, 64, 100, 128, 256, 512, 1024]:
                    total_files = folder_count * files_per_folder

                    if total_files > 0:
                        file_size_mb = total_data_mb / total_files

                        # Filter for practical file sizes
                        if 0.1 <= file_size_mb <= 1024:
                            combinations.append((folder_count, files_per_folder, file_size_mb, strategy))

    return combinations


def generate_benchmark_parameters(total_data_sizes_mb: List[int]) -> List[BenchmarkParams]:
    """Generate comprehensive benchmark parameters for given data sizes"""
    all_params = []

    for total_data_mb in total_data_sizes_mb:
        print(f"\nGenerating parameters for {total_data_mb}MB total data:")
        print("=" * 70)

        # Get host/thread combinations
        host_thread_combos = generate_host_thread_combinations(total_data_mb)

        # Create parameters for each host/thread combination
        for data_per_host, hosts, threads_per_host, data_per_thread in host_thread_combos:

            # Get file structure combinations for this host count
            file_structure_combos = generate_file_structure_combinations(total_data_mb, hosts)

            # Create all combinations
            for folder_count, files_per_folder, file_size, strategy in file_structure_combos:
                # Verify the math works out
                calculated_total = folder_count * files_per_folder * file_size
                if abs(calculated_total - total_data_mb) < 0.01:  # Allow small floating point errors

                    # Additional validation for dedicated folder strategy
                    if strategy == 'dedicated' and folder_count % hosts != 0:
                        continue  # Skip if folders can't be evenly divided among hosts

                    params = BenchmarkParams(
                        total_data_mb=total_data_mb,
                        data_per_host_mb=data_per_host,
                        host_count=hosts,
                        threads_per_host=threads_per_host,
                        data_per_thread_mb=data_per_thread,
                        folder_count=folder_count,
                        files_per_folder=files_per_folder,
                        file_size_mb=file_size,
                        host_folder_strategy=strategy
                    )
                    all_params.append(params)

        # Sort by host count, then thread count, then folder strategy for better readability
        size_params = [p for p in all_params if p.total_data_mb == total_data_mb]
        size_params.sort(key=lambda x: (x.host_count, x.threads_per_host, x.host_folder_strategy, x.folder_count))

        # Print sample of parameters for this data size
        print(f"Generated {len(size_params)} parameter combinations")
        print("\nSample configurations:")
        for i, params in enumerate(size_params[:15]):  # Show first 15
            print(f"  {i+1:2d}. {params}")
        if len(size_params) > 15:
            print(f"  ... and {len(size_params) - 15} more configurations")

    return all_params


def filter_practical_parameters(params: List[BenchmarkParams]) -> List[BenchmarkParams]:
    """Filter parameters to remove impractical configurations"""
    filtered = []

    for p in params:
        # Skip configurations with too many threads per host (>64 is often impractical)
        if p.threads_per_host > 64:
            continue

        # Skip configurations with too many total threads (>512 might be excessive)
        if p.total_threads > 512:
            continue

        # Skip configurations with too many hosts (>64 might be impractical for most setups)
        if p.host_count > 64:
            continue

        # Skip configurations with too many folders (>10000 folders might be excessive)
        if p.folder_count > 10000:
            continue

        # Skip configurations with too many files per folder (>10000 might be excessive)
        if p.files_per_folder > 10000:
            continue

        # Skip very small file sizes (< 0.5MB might not be representative)
        if p.file_size_mb < 0.5:
            continue

        # Skip configurations where data per thread is too small (< 1MB)
        if p.data_per_thread_mb < 1:
            continue

        filtered.append(p)

    return filtered


def export_to_csv(params: List[BenchmarkParams], filename: str = "multi_host_benchmark_parameters.csv"):
    """Export parameters to CSV file"""
    import csv

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['total_data_mb', 'data_per_host_mb', 'host_count', 'threads_per_host',
                      'data_per_thread_mb', 'total_threads', 'folder_count', 'files_per_folder',
                      'file_size_mb', 'total_files', 'host_folder_strategy']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for p in params:
            writer.writerow({
                'total_data_mb': p.total_data_mb,
                'data_per_host_mb': p.data_per_host_mb,
                'host_count': p.host_count,
                'threads_per_host': p.threads_per_host,
                'data_per_thread_mb': p.data_per_thread_mb,
                'total_threads': p.total_threads,
                'folder_count': p.folder_count,
                'files_per_folder': p.files_per_folder,
                'file_size_mb': round(p.file_size_mb, 4),
                'total_files': p.total_files,
                'host_folder_strategy': p.host_folder_strategy
            })

    print(f"\nExported {len(params)} parameter sets to {filename}")


def analyze_configurations(params: List[BenchmarkParams]):
    """Analyze and show insights about the generated configurations"""
    print("\nConfiguration Analysis:")
    print("=" * 50)

    # Group by strategy
    strategies = {}
    for p in params:
        if p.host_folder_strategy not in strategies:
            strategies[p.host_folder_strategy] = []
        strategies[p.host_folder_strategy].append(p)

    for strategy, strategy_params in strategies.items():
        print(f"\n{strategy.upper()} Strategy ({len(strategy_params)} configs):")

        if strategy == 'shared':
            print("  - All hosts write to same folders (high contention)")
            print("  - Tests shared storage under concurrent access")

        elif strategy == 'dedicated':
            print("  - Each host writes to separate folders (low contention)")
            print("  - Tests storage scalability with isolated access patterns")

        elif strategy == 'mixed':
            print("  - Hosts use mixed folder access patterns")
            print("  - Tests realistic workload scenarios")

        # Show host distribution
        host_counts = sorted(set(p.host_count for p in strategy_params))
        print(f"  - Host counts: {host_counts}")

        # Show thread distribution
        max_threads = max(p.total_threads for p in strategy_params)
        min_threads = min(p.total_threads for p in strategy_params)
        print(f"  - Total threads range: {min_threads}-{max_threads}")


def generate_test_scenarios(params: List[BenchmarkParams]) -> dict:
    """Generate specific test scenario recommendations"""
    scenarios = {
        'contention_test': [],
        'scalability_test': [],
        'mixed_workload': [],
        'single_host_baseline': []
    }

    for p in params:
        # Single host baseline
        if p.host_count == 1:
            scenarios['single_host_baseline'].append(p)

        # High contention test (shared folders, multiple hosts)
        elif p.host_folder_strategy == 'shared' and p.host_count >= 4:
            scenarios['contention_test'].append(p)

        # Scalability test (dedicated folders, scaling hosts)
        elif p.host_folder_strategy == 'dedicated' and p.host_count >= 2:
            scenarios['scalability_test'].append(p)

        # Mixed workload (mixed strategy)
        elif p.host_folder_strategy == 'mixed':
            scenarios['mixed_workload'].append(p)

    return scenarios


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

    print("Multi-Host Storage Benchmark Parameter Generator")
    print("===============================================")

    # Generate all parameters
    all_params = generate_benchmark_parameters(data_sizes)

    # Filter to practical parameters
    practical_params = filter_practical_parameters(all_params)

    print(f"\nSummary:")
    print(f"Total parameter combinations: {len(all_params)}")
    print(f"Practical parameter combinations: {len(practical_params)}")

    # Analyze configurations
    analyze_configurations(practical_params)

    # Export to CSV
    export_to_csv(practical_params)

    # Generate test scenarios
    scenarios = generate_test_scenarios(practical_params)

    print(f"\nRecommended Test Scenarios:")
    print("=" * 50)

    for scenario_name, scenario_params in scenarios.items():
        if scenario_params:
            print(f"\n{scenario_name.replace('_', ' ').title()} ({len(scenario_params)} configs):")
            # Show a few examples
            for i, p in enumerate(sorted(scenario_params, key=lambda x: (x.host_count, x.total_threads))[:3]):
                print(f"  {i+1}. {p}")
            if len(scenario_params) > 3:
                print(f"  ... and {len(scenario_params) - 3} more")

    # Show some multi-host specific examples
    print(f"\nMulti-Host Scaling Examples:")
    print("-" * 80)

    for size in [1024, 4096]:  # Show examples for 1GB and 4GB
        size_params = [p for p in practical_params if p.total_data_mb == size and p.host_count > 1]
        if size_params:
            print(f"\n{size}MB across multiple hosts:")

            # Show scaling examples
            host_scaling = {}
            for p in size_params:
                key = (p.threads_per_host, p.host_folder_strategy)
                if key not in host_scaling:
                    host_scaling[key] = []
                host_scaling[key].append(p)

            # Show one example of each scaling pattern
            shown = 0
            for (threads, strategy), configs in host_scaling.items():
                if shown < 4:  # Limit examples
                    configs.sort(key=lambda x: x.host_count)
                    example = configs[len(configs)//2]  # Pick middle example
                    print(f"  {example}")
                    shown += 1


if __name__ == "__main__":
    main()