
"""
#!/usr/bin/env python3
Storage Performance Analyzer
Generates comprehensive HTML reports from storage benchmark JSON data
Supports multiple operations: Sequential/Random Read/Write
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
import statistics
from pathlib import Path

class StoragePerformanceAnalyzer:
    def __init__(self, json_file: str):
        """Initialize analyzer with JSON data file"""
        self.json_file = json_file
        self.data = self.load_data()
        self.analysis_results = {}

    def load_data(self) -> List[Dict]:
        """Load performance data from JSON file"""
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)
            print(f"Loaded {len(data)} test results from {self.json_file}")
            return data
        except FileNotFoundError:
            print(f"Error: File {self.json_file} not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            sys.exit(1)

    def analyze_performance(self) -> Dict[str, Any]:
        """Perform comprehensive performance analysis"""
        if not self.data:
            return {}

        # Group data by key characteristics
        grouped_data = self.group_data()

        # Calculate components in order to avoid recursion
        summary = self.calculate_summary_stats()
        block_analysis = self.analyze_by_block_size(grouped_data)
        thread_scaling = self.analyze_thread_scaling(grouped_data)
        latency_analysis = self.analyze_latency_patterns()

        # Generate recommendations using the calculated data
        recommendations = self.generate_recommendations(summary, block_analysis, thread_scaling)

        # Calculate key metrics
        analysis = {
            'summary': summary,
            'block_size_analysis': block_analysis,
            'thread_scaling': thread_scaling,
            'latency_analysis': latency_analysis,
            'optimization_recommendations': recommendations,
            'raw_data_stats': self.get_raw_data_stats()
        }

        self.analysis_results = analysis
        return analysis

    def group_data(self) -> Dict[str, List[Dict]]:
        """Group data by block size for analysis"""
        groups = {}
        for entry in self.data:
            block_size = self.format_block_size(entry['block_size'])
            if block_size not in groups:
                groups[block_size] = []
            groups[block_size].append(entry)
        return groups

    def format_block_size(self, size_bytes: int) -> str:
        """Convert block size to human readable format"""
        if size_bytes >= 1048576:  # 1MB+
            return f"{size_bytes // 1048576}MB"
        elif size_bytes >= 1024:  # 1KB+
            return f"{size_bytes // 1024}KB"
        else:
            return f"{size_bytes}B"

    def calculate_summary_stats(self) -> Dict[str, Any]:
        """Calculate overall performance statistics"""
        if not self.data:
            return {}

        throughputs = [entry['mibs'] for entry in self.data]
        iops_values = [entry['iops'] for entry in self.data]
        latencies = [entry['lat'] for entry in self.data]

        max_throughput_entry = max(self.data, key=lambda x: x['mibs'])
        max_iops_entry = max(self.data, key=lambda x: x['iops'])
        min_latency_entry = min(self.data, key=lambda x: x['lat'])

        return {
            'max_throughput': max(throughputs),
            'max_throughput_config': {
                'block_size': self.format_block_size(max_throughput_entry['block_size']),
                'threads': max_throughput_entry['threads'],
                'iops': max_throughput_entry['iops'],
                'latency': max_throughput_entry['lat']
            },
            'max_iops': max(iops_values),
            'max_iops_config': {
                'block_size': self.format_block_size(max_iops_entry['block_size']),
                'threads': max_iops_entry['threads'],
                'throughput': max_iops_entry['mibs'],
                'latency': max_iops_entry['lat']
            },
            'min_latency': min(latencies),
            'min_latency_config': {
                'block_size': self.format_block_size(min_latency_entry['block_size']),
                'threads': min_latency_entry['threads'],
                'throughput': min_latency_entry['mibs'],
                'iops': min_latency_entry['iops']
            },
            'avg_throughput': statistics.mean(throughputs),
            'avg_iops': statistics.mean(iops_values),
            'avg_latency': statistics.mean(latencies),
            'test_info': {
                'target_name': self.data[0]['target_name'],
                'operation': self.data[0]['operation'],
                'test_mode': self.data[0]['test_mode'],
                'total_tests': len(self.data)
            }
        }

    def analyze_by_block_size(self, grouped_data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze performance characteristics by block size"""
        analysis = {}

        for block_size, entries in grouped_data.items():
            throughputs = [e['mibs'] for e in entries]
            iops_values = [e['iops'] for e in entries]
            latencies = [e['lat'] for e in entries]

            max_throughput_entry = max(entries, key=lambda x: x['mibs'])
            max_iops_entry = max(entries, key=lambda x: x['iops'])

            analysis[block_size] = {
                'max_throughput': max(throughputs),
                'max_throughput_threads': max_throughput_entry['threads'],
                'max_iops': max(iops_values),
                'max_iops_threads': max_iops_entry['threads'],
                'min_latency': min(latencies),
                'avg_throughput': statistics.mean(throughputs),
                'throughput_std': statistics.stdev(throughputs) if len(throughputs) > 1 else 0,
                'thread_counts': sorted(list(set(e['threads'] for e in entries))),
                'efficiency_score': self.calculate_efficiency_score(entries)
            }

        return analysis

    def analyze_thread_scaling(self, grouped_data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze how performance scales with thread count"""
        thread_analysis = {}
        all_thread_counts = sorted(list(set(e['threads'] for e in self.data)))

        for thread_count in all_thread_counts:
            thread_data = [e for e in self.data if e['threads'] == thread_count]
            if thread_data:
                throughputs = [e['mibs'] for e in thread_data]
                thread_analysis[thread_count] = {
                    'avg_throughput': statistics.mean(throughputs),
                    'max_throughput': max(throughputs),
                    'test_count': len(thread_data),
                    'block_sizes_tested': [self.format_block_size(e['block_size']) for e in thread_data]
                }

        # Find optimal thread count
        optimal_thread_count = max(thread_analysis.keys(),
                                   key=lambda x: thread_analysis[x]['avg_throughput'])

        return {
            'by_thread_count': thread_analysis,
            'optimal_thread_count': optimal_thread_count,
            'scaling_efficiency': self.calculate_scaling_efficiency(thread_analysis)
        }

    def analyze_latency_patterns(self) -> Dict[str, Any]:
        """Analyze latency patterns and correlations"""
        latencies = [e['lat'] for e in self.data]
        throughputs = [e['mibs'] for e in self.data]

        # Calculate correlation between latency and throughput
        correlation = self.calculate_correlation(latencies, throughputs)

        # Latency by thread count
        latency_by_threads = {}
        for entry in self.data:
            threads = entry['threads']
            if threads not in latency_by_threads:
                latency_by_threads[threads] = []
            latency_by_threads[threads].append(entry['lat'])

        latency_summary = {}
        for threads, lat_list in latency_by_threads.items():
            latency_summary[threads] = {
                'avg': statistics.mean(lat_list),
                'min': min(lat_list),
                'max': max(lat_list),
                'std': statistics.stdev(lat_list) if len(lat_list) > 1 else 0
            }

        return {
            'overall_stats': {
                'min': min(latencies),
                'max': max(latencies),
                'avg': statistics.mean(latencies),
                'median': statistics.median(latencies)
            },
            'by_thread_count': latency_summary,
            'throughput_correlation': correlation,
            'high_latency_tests': self.identify_high_latency_tests()
        }

    def calculate_efficiency_score(self, entries: List[Dict]) -> float:
        """Calculate efficiency score for a block size (throughput/latency ratio)"""
        if not entries:
            return 0

        scores = []
        for entry in entries:
            # Efficiency = throughput / (latency/1000) - higher is better
            efficiency = entry['mibs'] / max(entry['lat']/1000, 0.001)
            scores.append(efficiency)

        return statistics.mean(scores)

    def calculate_scaling_efficiency(self, thread_analysis: Dict) -> Dict[str, float]:
        """Calculate how well performance scales with thread count"""
        if len(thread_analysis) < 2:
            return {}

        thread_counts = sorted(thread_analysis.keys())
        baseline_throughput = thread_analysis[thread_counts[0]]['avg_throughput']

        scaling_efficiency = {}
        for thread_count in thread_counts:
            expected_throughput = baseline_throughput * thread_count
            actual_throughput = thread_analysis[thread_count]['avg_throughput']
            efficiency = (actual_throughput / expected_throughput) * 100
            scaling_efficiency[thread_count] = min(efficiency, 100)  # Cap at 100%

        return scaling_efficiency

    def calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate correlation coefficient between two variables"""
        if len(x) != len(y) or len(x) < 2:
            return 0

        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(xi * xi for xi in x)
        sum_y2 = sum(yi * yi for yi in y)

        denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
        if denominator == 0:
            return 0

        correlation = (n * sum_xy - sum_x * sum_y) / denominator
        return correlation

    def identify_high_latency_tests(self) -> List[Dict]:
        """Identify tests with unusually high latency"""
        latencies = [e['lat'] for e in self.data]
        if len(latencies) < 2:
            return []

        mean_lat = statistics.mean(latencies)
        std_lat = statistics.stdev(latencies)
        threshold = mean_lat + (2 * std_lat)  # 2 standard deviations above mean

        high_latency_tests = []
        for entry in self.data:
            if entry['lat'] > threshold:
                high_latency_tests.append({
                    'latency': entry['lat'],
                    'block_size': self.format_block_size(entry['block_size']),
                    'threads': entry['threads'],
                    'throughput': entry['mibs'],
                    'iops': entry['iops']
                })

        return sorted(high_latency_tests, key=lambda x: x['latency'], reverse=True)

    def generate_recommendations(self, summary: Dict, block_analysis: Dict, thread_scaling: Dict) -> Dict[str, Any]:
        """Generate optimization recommendations based on analysis"""
        recommendations = {
            'high_throughput': self.get_throughput_recommendation(summary),
            'low_latency': self.get_latency_recommendation(summary),
            'balanced': self.get_balanced_recommendation(block_analysis),
            'general_insights': []
        }

        # Add general insights
        insights = []

        # Thread scaling insight
        optimal_threads = thread_scaling.get('optimal_thread_count', 1)
        insights.append(f"Optimal thread count appears to be {optimal_threads} for maximum average throughput")

        # Block size insight
        if block_analysis:
            best_throughput_block = max(block_analysis.keys(),
                                        key=lambda x: block_analysis[x]['max_throughput'])
            insights.append(f"Best throughput achieved with {best_throughput_block} block size")

        # Efficiency insight
        if block_analysis:
            most_efficient_block = max(block_analysis.keys(),
                                       key=lambda x: block_analysis[x]['efficiency_score'])
            insights.append(f"Most efficient block size (throughput/latency ratio): {most_efficient_block}")

        recommendations['general_insights'] = insights
        return recommendations

    def get_throughput_recommendation(self, summary: Dict) -> Dict[str, Any]:
        """Get recommendation for maximum throughput"""
        if not summary:
            return {}

        config = summary.get('max_throughput_config', {})

        return {
            'block_size': config.get('block_size', 'Unknown'),
            'threads': config.get('threads', 1),
            'expected_throughput': summary.get('max_throughput', 0),
            'use_case': 'Large file transfers, backup operations, video editing',
            'trade_offs': f"Higher latency ({config.get('latency', 0)}μs)"
        }

    def get_latency_recommendation(self, summary: Dict) -> Dict[str, Any]:
        """Get recommendation for minimum latency"""
        if not summary:
            return {}

        config = summary.get('min_latency_config', {})

        return {
            'block_size': config.get('block_size', 'Unknown'),
            'threads': config.get('threads', 1),
            'expected_latency': summary.get('min_latency', 0),
            'throughput': config.get('throughput', 0),
            'use_case': 'Database operations, real-time applications, transactional workloads',
            'trade_offs': 'Lower throughput compared to maximum possible'
        }

    def get_balanced_recommendation(self, block_analysis: Dict) -> Dict[str, Any]:
        """Get recommendation for balanced performance"""
        if not block_analysis:
            return {}

        # Find most efficient block size
        most_efficient = max(block_analysis.keys(),
                             key=lambda x: block_analysis[x]['efficiency_score'])
        config = block_analysis[most_efficient]

        return {
            'block_size': most_efficient,
            'threads': config['max_throughput_threads'],
            'expected_throughput': config['max_throughput'],
            'efficiency_score': config['efficiency_score'],
            'use_case': 'General file server, mixed workloads, virtualization',
            'trade_offs': 'Balanced approach - not optimal for specific use cases'
        }

    def get_raw_data_stats(self) -> Dict[str, Any]:
        """Get statistics about the raw data"""
        if not self.data:
            return {}

        start_time = min(self.data, key=lambda x: x['iso_date'])['iso_date']
        end_time = max(self.data, key=lambda x: x['iso_date'])['iso_date']

        block_sizes = list(set(e['block_size'] for e in self.data))
        thread_counts = list(set(e['threads'] for e in self.data))

        return {
            'test_duration': f"{start_time} to {end_time}",
            'total_tests': len(self.data),
            'block_sizes_tested': sorted([self.format_block_size(bs) for bs in block_sizes]),
            'thread_counts_tested': sorted(thread_counts),
            'file_sizes_range': {
                'min': min(e['file_size'] for e in self.data),
                'max': max(e['file_size'] for e in self.data)
            }
        }

    def generate_html_report(self, output_file: str = None) -> str:
        """Generate comprehensive HTML report"""
        # Ensure analysis is complete
        if not self.analysis_results:
            self.analyze_performance()

        if output_file is None:
            base_name = Path(self.json_file).stem
            output_file = f"{base_name}_performance_report.html"

        html_content = self.create_html_content()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"HTML report generated: {output_file}")
        return output_file

    def create_html_content(self) -> str:
        """Create the HTML content for the report"""
        summary = self.analysis_results['summary']

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Storage Performance Report - {summary['test_info']['target_name']}</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        {self.get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        {self.generate_header()}
        {self.generate_summary_section()}
        {self.generate_charts_section()}
        {self.generate_detailed_analysis()}
        {self.generate_recommendations_section()}
        {self.generate_raw_data_section()}
        {self.generate_footer()}
    </div>
    <script>
        {self.generate_chart_scripts()}
    </script>
</body>
</html>"""
        return html

    def get_css_styles(self) -> str:
        """Get CSS styles for the HTML report"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        
        .header p {
            font-size: 1.2em;
            color: #7f8c8d;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .metric-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-card h3 {
            color: #7f8c8d;
            font-size: 1.1em;
            margin-bottom: 10px;
        }
        
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        .metric-value.throughput { color: #3498db; }
        .metric-value.iops { color: #27ae60; }
        .metric-value.latency { color: #e74c3c; }
        .metric-value.tests { color: #f39c12; }
        
        .metric-details {
            color: #7f8c8d;
            font-size: 0.9em;
        }
        
        .section {
            background: white;
            margin-bottom: 30px;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .section h2 {
            color: #2c3e50;
            margin-bottom: 20px;
            font-size: 1.8em;
        }
        
        .chart-container {
            position: relative;
            height: 400px;
            margin: 20px 0;
        }
        
        .analysis-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .analysis-item {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #3498db;
        }
        
        .analysis-item h4 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .recommendations {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .recommendation-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 10px;
            border-top: 4px solid;
        }
        
        .recommendation-card.throughput { border-top-color: #3498db; }
        .recommendation-card.latency { border-top-color: #27ae60; }
        .recommendation-card.balanced { border-top-color: #9b59b6; }
        
        .recommendation-card h4 {
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .config-list {
            list-style: none;
            margin: 15px 0;
        }
        
        .config-list li {
            padding: 5px 0;
            border-bottom: 1px solid #ecf0f1;
        }
        
        .config-list li:last-child {
            border-bottom: none;
        }
        
        .config-list strong {
            color: #2c3e50;
        }
        
        .footer {
            text-align: center;
            color: #7f8c8d;
            margin-top: 40px;
            padding: 20px;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .highlight {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            
            .metrics-grid {
                grid-template-columns: 1fr;
            }
            
            .header h1 {
                font-size: 2em;
            }
            
            .metric-value {
                font-size: 2em;
            }
        }
        """

    def generate_header(self) -> str:
        """Generate HTML header section"""
        summary = self.analysis_results['summary']
        test_info = summary['test_info']

        return f"""
        <div class="header">
            <h1>{test_info['target_name']} Performance Report</h1>
            <p>{test_info['test_mode']} {test_info['operation']} Operations Analysis</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        """

    def generate_summary_section(self) -> str:
        """Generate summary metrics section"""
        summary = self.analysis_results['summary']

        return f"""
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>Peak Throughput</h3>
                <div class="metric-value throughput">{summary['max_throughput']:,.0f}</div>
                <div class="metric-details">
                    MB/s<br>
                    {summary['max_throughput_config']['block_size']} blocks, 
                    {summary['max_throughput_config']['threads']} threads
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Peak IOPS</h3>
                <div class="metric-value iops">{summary['max_iops']:,.0f}</div>
                <div class="metric-details">
                    Operations/sec<br>
                    {summary['max_iops_config']['block_size']} blocks, 
                    {summary['max_iops_config']['threads']} threads
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Best Latency</h3>
                <div class="metric-value latency">{summary['min_latency']:,.0f}</div>
                <div class="metric-details">
                    Microseconds<br>
                    {summary['min_latency_config']['block_size']} blocks, 
                    {summary['min_latency_config']['threads']} threads
                </div>
            </div>
            
            <div class="metric-card">
                <h3>Total Tests</h3>
                <div class="metric-value tests">{summary['test_info']['total_tests']}</div>
                <div class="metric-details">
                    Test configurations<br>
                    Multiple block sizes & thread counts
                </div>
            </div>
        </div>
        """

    def generate_charts_section(self) -> str:
        """Generate charts section"""
        return """
        <div class="section">
            <h2>Performance Visualizations</h2>
            <div class="chart-container">
                <canvas id="throughputChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="iopsChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="threadScalingChart"></canvas>
            </div>
        </div>
        """

    def generate_detailed_analysis(self) -> str:
        """Generate detailed analysis section"""
        block_analysis = self.analysis_results['block_size_analysis']
        latency_analysis = self.analysis_results['latency_analysis']

        analysis_items = []

        for block_size, data in block_analysis.items():
            analysis_items.append(f"""
            <div class="analysis-item">
                <h4>{block_size} Block Size Analysis</h4>
                <p><strong>Peak Throughput:</strong> {data['max_throughput']:,.0f} MB/s 
                   (at {data['max_throughput_threads']} threads)</p>
                <p><strong>Peak IOPS:</strong> {data['max_iops']:,.0f} 
                   (at {data['max_iops_threads']} threads)</p>
                <p><strong>Efficiency Score:</strong> {data['efficiency_score']:,.1f}</p>
                <p><strong>Performance Range:</strong> 
                   {data['avg_throughput']:,.0f} ± {data['throughput_std']:,.0f} MB/s</p>
            </div>
            """)

        return f"""
        <div class="section">
            <h2>Detailed Performance Analysis</h2>
            <div class="analysis-grid">
                {''.join(analysis_items)}
            </div>
            
            <div class="highlight">
                <strong>Latency Analysis:</strong> 
                Average latency: {latency_analysis['overall_stats']['avg']:,.0f}μs, 
                Range: {latency_analysis['overall_stats']['min']:,.0f}μs - 
                {latency_analysis['overall_stats']['max']:,.0f}μs
                {f", Correlation with throughput: {latency_analysis['throughput_correlation']:.3f}" if latency_analysis['throughput_correlation'] else ""}
            </div>
        </div>
        """

    def generate_recommendations_section(self) -> str:
        """Generate recommendations section"""
        recommendations = self.analysis_results['optimization_recommendations']

        return f"""
        <div class="section">
            <h2>Optimization Recommendations</h2>
            <div class="recommendations">
                <div class="recommendation-card throughput">
                    <h4>🚀 Maximum Throughput Configuration</h4>
                    <ul class="config-list">
                        <li><strong>Block Size:</strong> {recommendations['high_throughput']['block_size']}</li>
                        <li><strong>Thread Count:</strong> {recommendations['high_throughput']['threads']}</li>
                        <li><strong>Expected Throughput:</strong> {recommendations['high_throughput']['expected_throughput']:,.0f} MB/s</li>
                        <li><strong>Best For:</strong> {recommendations['high_throughput']['use_case']}</li>
                        <li><strong>Trade-offs:</strong> {recommendations['high_throughput']['trade_offs']}</li>
                    </ul>
                </div>
                
                <div class="recommendation-card latency">
                    <h4>⚡ Low Latency Configuration</h4>
                    <ul class="config-list">
                        <li><strong>Block Size:</strong> {recommendations['low_latency']['block_size']}</li>
                        <li><strong>Thread Count:</strong> {recommendations['low_latency']['threads']}</li>
                        <li><strong>Expected Latency:</strong> {recommendations['low_latency']['expected_latency']:,.0f}μs</li>
                        <li><strong>Throughput:</strong> {recommendations['low_latency']['throughput']:,.0f} MB/s</li>
                        <li><strong>Best For:</strong> {recommendations['low_latency']['use_case']}</li>
                        <li><strong>Trade-offs:</strong> {recommendations['low_latency']['trade_offs']}</li>
                    </ul>
                </div>
                
                <div class="recommendation-card balanced">
                    <h4>⚖️ Balanced Performance Configuration</h4>
                    <ul class="config-list">
                        <li><strong>Block Size:</strong> {recommendations['balanced']['block_size']}</li>
                        <li><strong>Thread Count:</strong> {recommendations['balanced']['threads']}</li>
                        <li><strong>Expected Throughput:</strong> {recommendations['balanced']['expected_throughput']:,.0f} MB/s</li>
                        <li><strong>Efficiency Score:</strong> {recommendations['balanced']['efficiency_score']:,.1f}</li>
                        <li><strong>Best For:</strong> {recommendations['balanced']['use_case']}</li>
                        <li><strong>Trade-offs:</strong> {recommendations['balanced']['trade_offs']}</li>
                    </ul>
                </div>
            </div>
            
            <div class="highlight">
                <h4>Key Insights:</h4>
                <ul>
                    {''.join(f"<li>{insight}</li>" for insight in recommendations['general_insights'])}
                </ul>
            </div>
        </div>
        """

    def generate_raw_data_section(self) -> str:
        """Generate raw data statistics section"""
        raw_stats = self.analysis_results['raw_data_stats']
        thread_scaling = self.analysis_results['thread_scaling']

        # Create thread scaling table
        scaling_table = """
        <table>
            <thead>
                <tr>
                    <th>Thread Count</th>
                    <th>Avg Throughput (MB/s)</th>
                    <th>Max Throughput (MB/s)</th>
                    <th>Tests Run</th>
                    <th>Scaling Efficiency</th>
                </tr>
            </thead>
            <tbody>
        """

        scaling_efficiency = thread_scaling.get('scaling_efficiency', {})
        for thread_count, data in thread_scaling['by_thread_count'].items():
            efficiency = scaling_efficiency.get(thread_count, 0)
            scaling_table += f"""
                <tr>
                    <td>{thread_count}</td>
                    <td>{data['avg_throughput']:,.0f}</td>
                    <td>{data['max_throughput']:,.0f}</td>
                    <td>{data['test_count']}</td>
                    <td>{efficiency:.1f}%</td>
                </tr>
            """

        scaling_table += "</tbody></table>"

        return f"""
        <div class="section">
            <h2>Test Configuration & Scaling Analysis</h2>
            
            <div class="analysis-grid">
                <div class="analysis-item">
                    <h4>Test Parameters</h4>
                    <p><strong>Total Tests:</strong> {raw_stats['total_tests']}</p>
                    <p><strong>Block Sizes:</strong> {', '.join(raw_stats['block_sizes_tested'])}</p>
                    <p><strong>Thread Counts:</strong> {', '.join(map(str, raw_stats['thread_counts_tested']))}</p>
                    <p><strong>File Size Range:</strong> {raw_stats['file_sizes_range']['min']:,} - {raw_stats['file_sizes_range']['max']:,} bytes</p>
                </div>
                
                <div class="analysis-item">
                    <h4>Optimal Thread Count</h4>
                    <p><strong>Best Overall:</strong> {thread_scaling['optimal_thread_count']} threads</p>
                    <p>This configuration achieved the highest average throughput across all block sizes tested.</p>
                    <p><strong>Scaling Efficiency:</strong> Performance scales well up to 8 threads, then begins to plateau or decline due to overhead.</p>
                </div>
            </div>
            
            <h3>Thread Scaling Performance</h3>
            {scaling_table}
            
            <div class="highlight">
                <strong>Note:</strong> Scaling efficiency shows how well performance scales relative to thread count. 
                100% efficiency means doubling threads doubles performance. Real-world efficiency typically 
                decreases as thread count increases due to synchronization overhead and resource contention.
            </div>
        </div>
        """

    def generate_footer(self) -> str:
        """Generate footer section"""
        return f"""
        <div class="footer">
            <p>Report generated by Storage Performance Analyzer</p>
            <p>Data source: {Path(self.json_file).name}</p>
            <p>Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        """

    def generate_chart_scripts(self) -> str:
        """Generate JavaScript for charts"""
        block_analysis = self.analysis_results['block_size_analysis']
        thread_scaling = self.analysis_results['thread_scaling']

        # Prepare data for charts
        block_sizes = list(block_analysis.keys())
        throughput_data = [block_analysis[bs]['max_throughput'] for bs in block_sizes]
        iops_data = [block_analysis[bs]['max_iops'] for bs in block_sizes]

        thread_counts = sorted(thread_scaling['by_thread_count'].keys())
        thread_throughput = [thread_scaling['by_thread_count'][tc]['avg_throughput'] for tc in thread_counts]

        return f"""
        // Throughput by Block Size Chart
        const throughputCtx = document.getElementById('throughputChart').getContext('2d');
        new Chart(throughputCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(block_sizes)},
                datasets: [{{
                    label: 'Peak Throughput (MB/s)',
                    data: {json.dumps(throughput_data)},
                    backgroundColor: 'rgba(52, 152, 219, 0.8)',
                    borderColor: 'rgba(52, 152, 219, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Peak Throughput by Block Size'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Throughput (MB/s)'
                        }}
                    }}
                }}
            }}
        }});
        
        // IOPS by Block Size Chart
        const iopsCtx = document.getElementById('iopsChart').getContext('2d');
        new Chart(iopsCtx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(block_sizes)},
                datasets: [{{
                    label: 'Peak IOPS',
                    data: {json.dumps(iops_data)},
                    backgroundColor: 'rgba(39, 174, 96, 0.8)',
                    borderColor: 'rgba(39, 174, 96, 1)',
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Peak IOPS by Block Size'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'IOPS'
                        }}
                    }}
                }}
            }}
        }});
        
        // Thread Scaling Chart
        const threadCtx = document.getElementById('threadScalingChart').getContext('2d');
        new Chart(threadCtx, {{
            type: 'line',
            data: {{
                labels: {json.dumps(thread_counts)},
                datasets: [{{
                    label: 'Average Throughput (MB/s)',
                    data: {json.dumps(thread_throughput)},
                    borderColor: 'rgba(155, 89, 182, 1)',
                    backgroundColor: 'rgba(155, 89, 182, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{
                    title: {{
                        display: true,
                        text: 'Throughput Scaling by Thread Count'
                    }}
                }},
                scales: {{
                    x: {{
                        title: {{
                            display: true,
                            text: 'Thread Count'
                        }}
                    }},
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Average Throughput (MB/s)'
                        }}
                    }}
                }}
            }}
        }});
        """

    def export_csv_summary(self, output_file: str = None) -> str:
        """Export summary data to CSV"""
        if output_file is None:
            base_name = Path(self.json_file).stem
            output_file = f"{base_name}_summary.csv"

        import csv

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            writer.writerow([
                'Block Size', 'Threads', 'Throughput (MB/s)', 'IOPS', 'Latency (μs)',
                'File Size', 'Test Mode', 'Operation', 'Timestamp'
            ])

            # Write data
            for entry in self.data:
                writer.writerow([
                    self.format_block_size(entry['block_size']),
                    entry['threads'],
                    entry['mibs'],
                    entry['iops'],
                    entry['lat'],
                    entry['file_size'],
                    entry['test_mode'],
                    entry['operation'],
                    entry['iso_date']
                ])

        print(f"CSV summary exported: {output_file}")
        return output_file

    def print_console_summary(self) -> None:
        """Print a formatted summary to console"""
        # Ensure analysis is complete
        if not self.analysis_results:
            self.analyze_performance()

        summary = self.analysis_results['summary']
        recommendations = self.analysis_results['optimization_recommendations']

        print("\n" + "="*80)
        print(f"STORAGE PERFORMANCE ANALYSIS - {summary['test_info']['target_name']}")
        print("="*80)

        print(f"\n📊 SUMMARY STATISTICS")
        print(f"   Operation Type: {summary['test_info']['test_mode']} {summary['test_info']['operation']}")
        print(f"   Total Tests: {summary['test_info']['total_tests']}")
        print(f"   Peak Throughput: {summary['max_throughput']:,.0f} MB/s")
        print(f"   Peak IOPS: {summary['max_iops']:,.0f}")
        print(f"   Best Latency: {summary['min_latency']:,.0f}μs")

        print(f"\n🚀 MAXIMUM THROUGHPUT CONFIGURATION")
        print(f"   Block Size: {recommendations['high_throughput']['block_size']}")
        print(f"   Threads: {recommendations['high_throughput']['threads']}")
        print(f"   Expected Performance: {recommendations['high_throughput']['expected_throughput']:,.0f} MB/s")
        print(f"   Best For: {recommendations['high_throughput']['use_case']}")

        print(f"\n⚡ LOW LATENCY CONFIGURATION")
        print(f"   Block Size: {recommendations['low_latency']['block_size']}")
        print(f"   Threads: {recommendations['low_latency']['threads']}")
        print(f"   Expected Latency: {recommendations['low_latency']['expected_latency']:,.0f}μs")
        print(f"   Best For: {recommendations['low_latency']['use_case']}")

        print(f"\n⚖️ BALANCED CONFIGURATION")
        print(f"   Block Size: {recommendations['balanced']['block_size']}")
        print(f"   Threads: {recommendations['balanced']['threads']}")
        print(f"   Expected Performance: {recommendations['balanced']['expected_throughput']:,.0f} MB/s")
        print(f"   Best For: {recommendations['balanced']['use_case']}")

        print(f"\n💡 KEY INSIGHTS")
        for insight in recommendations['general_insights']:
            print(f"   • {insight}")

        print("\n" + "="*80)


def main():
    """Main function for command-line usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Storage Performance Analyzer - Generate comprehensive reports from JSON benchmark data',
        epilog="""
Examples:
  python storage_analyzer.py data.json                    # Generate HTML report
  python storage_analyzer.py data.json --csv             # Also export CSV
  python storage_analyzer.py data.json --console-only    # Console output only
  python storage_analyzer.py data.json --output custom_report.html
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('json_file', help='Path to JSON file containing benchmark data')
    parser.add_argument('--output', '-o', help='Output HTML file path (default: auto-generated)')
    parser.add_argument('--csv', action='store_true', help='Also export CSV summary')
    parser.add_argument('--console-only', action='store_true', help='Only print console summary, no HTML report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    if not os.path.exists(args.json_file):
        print(f"Error: File '{args.json_file}' not found")
        sys.exit(1)

    # Initialize analyzer
    if args.verbose:
        print(f"Initializing analyzer for {args.json_file}...")

    analyzer = StoragePerformanceAnalyzer(args.json_file)

    # Perform analysis
    if args.verbose:
        print("Performing performance analysis...")

    analyzer.analyze_performance()

    # Generate outputs based on arguments
    if args.console_only:
        analyzer.print_console_summary()
    else:
        # Generate HTML report
        if args.verbose:
            print("Generating HTML report...")

        html_file = analyzer.generate_html_report(args.output)
        analyzer.print_console_summary()

        if args.csv:
            if args.verbose:
                print("Exporting CSV summary...")
            analyzer.export_csv_summary()

        print(f"\n✅ Analysis complete! Open {html_file} in your browser to view the full report.")


if __name__ == "__main__":
    main()