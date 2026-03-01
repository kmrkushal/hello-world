#!/usr/bin/env python3
"""
Example usage of the BENCH parser.
Demonstrates how to use the parser programmatically.
"""

from bench_parser import BenchParser

# Create a parser instance
parser = BenchParser()

# Parse a BENCH file
parser.parse_file('test_circuit.bench')

# Get information about a specific gate
gate_info = parser.get_gate_info('X1')
print(f"\nGate X1 info: {gate_info}")

# Get all gates
all_gates = parser.get_all_gates()
print(f"\nTotal gates: {len(all_gates)}")

# Get connections for a specific gate
connections = parser.get_connections('Cout')
print(f"\nGate 'Cout' is connected to: {connections}")

# Find all gates of a specific type
and_gates = parser.find_gates_by_type('AND')
print(f"\nAND gates found: {len(and_gates)}")
for gate in and_gates:
    print(f"  - {gate}")

# Get statistics
stats = parser.get_statistics()
print(f"\nStatistics: {stats}")

# Export to JSON
parser.export_to_json('circuit_info.json')
print("\nCircuit information exported to circuit_info.json")
