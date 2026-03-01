#!/usr/bin/env python3
"""
Benchmark script to estimate parsing time for large BENCH files.
"""

import time
import sys
from bench_parser import BenchParser

def generate_large_bench_file(filename: str, num_gates: int):
    """Generate a large BENCH file for testing."""
    print(f"Generating test file with ~{num_gates} gates...")
    
    with open(filename, 'w') as f:
        # Write inputs
        for i in range(10):
            f.write(f"INPUT(in{i})\n")
        
        # Write outputs
        for i in range(5):
            f.write(f"OUTPUT(out{i})\n")
        
        # Write gates
        for i in range(num_gates):
            # Alternate between different gate types and formats
            if i % 2 == 0:
                # Format: GATE(output, input1, input2)
                gate_type = ['AND', 'OR', 'NAND', 'NOR', 'XOR'][i % 5]
                f.write(f"{gate_type}(g{i}, in{i%10}, g{i-1 if i > 0 else 0})\n")
            else:
                # Format: output = GATE(input1, input2)
                gate_type = ['AND', 'OR', 'NAND', 'NOR', 'XOR'][i % 5]
                f.write(f"g{i} = {gate_type}(in{(i+1)%10}, g{i-1 if i > 0 else 0})\n")
    
    print(f"Generated {filename}")

def benchmark_parsing(filename: str):
    """Benchmark the parsing performance."""
    parser = BenchParser()
    
    start_time = time.time()
    parser.parse_file(filename)
    end_time = time.time()
    
    elapsed = end_time - start_time
    return elapsed, parser

if __name__ == '__main__':
    import os
    
    # Test with different file sizes
    test_sizes = [1000, 10000, 50000]  # Start with smaller sizes
    
    print("=== BENCH Parser Performance Benchmark ===\n")
    
    results = []
    
    for size in test_sizes:
        test_file = f"test_{size}.bench"
        
        # Generate test file
        generate_large_bench_file(test_file, size)
        
        # Benchmark parsing
        print(f"\nBenchmarking {size} gates...")
        elapsed, parser = benchmark_parsing(test_file)
        
        stats = parser.get_statistics()
        lines_approx = size + 15  # gates + inputs/outputs + comments
        
        results.append({
            'gates': size,
            'lines': lines_approx,
            'time': elapsed,
            'gates_per_sec': size / elapsed if elapsed > 0 else 0,
            'lines_per_sec': lines_approx / elapsed if elapsed > 0 else 0
        })
        
        print(f"  Time: {elapsed:.2f} seconds")
        print(f"  Gates/sec: {size/elapsed:.0f}")
        print(f"  Lines/sec: {lines_approx/elapsed:.0f}")
        
        # Clean up test file
        os.remove(test_file)
    
    # Estimate for 500k lines
    print("\n=== Extrapolation to 500,000 lines ===")
    
    if results:
        # Use average performance from tests
        avg_lines_per_sec = sum(r['lines_per_sec'] for r in results) / len(results)
        avg_gates_per_sec = sum(r['gates_per_sec'] for r in results) / len(results)
        
        # Assume 500k lines ≈ 500k gates (rough approximation)
        estimated_time_500k = 500000 / avg_lines_per_sec if avg_lines_per_sec > 0 else 0
        
        print(f"Average parsing speed: {avg_lines_per_sec:.0f} lines/sec")
        print(f"Average parsing speed: {avg_gates_per_sec:.0f} gates/sec")
        print(f"\nEstimated time for 500,000 lines: {estimated_time_500k:.1f} seconds")
        print(f"Estimated time for 500,000 lines: {estimated_time_500k/60:.1f} minutes")
        
        # Conservative estimate (account for larger files being slower)
        conservative_time = estimated_time_500k * 1.5
        print(f"\nConservative estimate (with overhead): {conservative_time:.1f} seconds")
        print(f"Conservative estimate: {conservative_time/60:.1f} minutes")
