#!/usr/bin/env python3
"""
BENCH Format Parser
Parses BENCH format files and stores gate information including:
- Gate type
- Gate name (output wire/node)
- Connections (which gates/nodes connect to this gate's inputs)
"""

import re
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Gate:
    """Represents a single gate in the circuit."""
    gate_type: str  # AND, OR, NAND, NOR, XOR, XNOR, NOT, etc.
    gate_name: str  # Output wire/node name
    inputs: List[str] = field(default_factory=list)  # Input wire/node names
    
    def __repr__(self):
        return f"Gate(type={self.gate_type}, name={self.gate_name}, inputs={self.inputs})"


class BenchParser:
    """Parser for BENCH format files."""
    
    # Gate types supported
    GATE_TYPES = {'AND', 'OR', 'NAND', 'NOR', 'XOR', 'XNOR', 'NOT', 'BUFF'}
    
    def __init__(self):
        self.gates: Dict[str, Gate] = {}  # gate_name -> Gate object
        self.inputs: Set[str] = set()  # Input node names
        self.outputs: Set[str] = set()  # Output node names
        self.all_nodes: Set[str] = set()  # All nodes (inputs, outputs, internal)
        
    def parse_file(self, filepath: str) -> None:
        """
        Parse a BENCH format file.
        
        Args:
            filepath: Path to the .bench file
        """
        print(f"Parsing BENCH file: {filepath}")
        
        with open(filepath, 'r') as f:
            line_count = 0
            for line in f:
                line_count += 1
                if line_count % 50000 == 0:
                    print(f"  Processed {line_count} lines...")
                
                # Remove leading/trailing whitespace
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse the line
                self._parse_line(line)
        
        print(f"Parsing complete. Processed {line_count} lines.")
        print(f"Found {len(self.inputs)} inputs, {len(self.outputs)} outputs, "
              f"{len(self.gates)} gates, {len(self.all_nodes)} total nodes.")
    
    def _parse_line(self, line: str) -> None:
        """Parse a single line of BENCH format."""
        # Pattern 1: INPUT(node_name) or OUTPUT(node_name)
        input_match = re.match(r'^INPUT\s*\(\s*(\w+)\s*\)', line, re.IGNORECASE)
        if input_match:
            node_name = input_match.group(1)
            self.inputs.add(node_name)
            self.all_nodes.add(node_name)
            return
        
        output_match = re.match(r'^OUTPUT\s*\(\s*(\w+)\s*\)', line, re.IGNORECASE)
        if output_match:
            node_name = output_match.group(1)
            self.outputs.add(node_name)
            self.all_nodes.add(node_name)
            return
        
        # Pattern 2: GATE_TYPE(output, input1, input2, ...)
        # Example: AND(A1, G1, G2)
        gate_match = re.match(r'^(\w+)\s*\(\s*(\w+)\s*,\s*(.+)\s*\)', line)
        if gate_match:
            gate_type = gate_match.group(1).upper()
            output_name = gate_match.group(2)
            inputs_str = gate_match.group(3)
            
            if gate_type in self.GATE_TYPES:
                inputs = [inp.strip() for inp in inputs_str.split(',')]
                self._add_gate(gate_type, output_name, inputs)
                return
        
        # Pattern 3: output = GATE_TYPE(input1, input2, ...)
        # Example: 10 = NAND(1, 3)
        assignment_match = re.match(r'^(\w+)\s*=\s*(\w+)\s*\(\s*(.+)\s*\)', line)
        if assignment_match:
            output_name = assignment_match.group(1)
            gate_type = assignment_match.group(2).upper()
            inputs_str = assignment_match.group(3)
            
            if gate_type in self.GATE_TYPES:
                inputs = [inp.strip() for inp in inputs_str.split(',')]
                self._add_gate(gate_type, output_name, inputs)
                return
    
    def _add_gate(self, gate_type: str, output_name: str, inputs: List[str]) -> None:
        """Add a gate to the circuit."""
        if output_name in self.gates:
            print(f"Warning: Gate '{output_name}' already exists. Overwriting...")
        
        gate = Gate(gate_type=gate_type, gate_name=output_name, inputs=inputs)
        self.gates[output_name] = gate
        
        # Track all nodes
        self.all_nodes.add(output_name)
        for inp in inputs:
            self.all_nodes.add(inp)
    
    def get_gate(self, gate_name: str) -> Optional[Gate]:
        """Get a gate by its name."""
        return self.gates.get(gate_name)
    
    def get_all_gates(self) -> Dict[str, Gate]:
        """Get all gates."""
        return self.gates
    
    def get_connections(self, gate_name: str) -> List[str]:
        """
        Get the list of nodes/gates that connect to this gate's inputs.
        
        Args:
            gate_name: Name of the gate
            
        Returns:
            List of input node names
        """
        gate = self.gates.get(gate_name)
        if gate:
            return gate.inputs
        return []
    
    def get_gate_info(self, gate_name: str) -> Optional[Dict]:
        """
        Get complete information about a gate.
        
        Returns:
            Dictionary with gate_type, gate_name, and connections
        """
        gate = self.gates.get(gate_name)
        if gate:
            return {
                'gate_type': gate.gate_type,
                'gate_name': gate.gate_name,
                'connections': gate.inputs
            }
        return None
    
    def get_all_gate_info(self) -> List[Dict]:
        """Get information about all gates."""
        return [
            {
                'gate_type': gate.gate_type,
                'gate_name': gate.gate_name,
                'connections': gate.inputs
            }
            for gate in self.gates.values()
        ]
    
    def find_gates_by_type(self, gate_type: str) -> List[Gate]:
        """Find all gates of a specific type."""
        return [gate for gate in self.gates.values() if gate.gate_type == gate_type.upper()]
    
    def get_statistics(self) -> Dict:
        """Get statistics about the parsed circuit."""
        gate_type_counts = defaultdict(int)
        for gate in self.gates.values():
            gate_type_counts[gate.gate_type] += 1
        
        return {
            'total_gates': len(self.gates),
            'total_inputs': len(self.inputs),
            'total_outputs': len(self.outputs),
            'total_nodes': len(self.all_nodes),
            'gate_type_counts': dict(gate_type_counts)
        }
    
    def export_to_dict(self) -> Dict:
        """Export all gate information to a dictionary."""
        return {
            'inputs': list(self.inputs),
            'outputs': list(self.outputs),
            'gates': {
                name: {
                    'gate_type': gate.gate_type,
                    'gate_name': gate.gate_name,
                    'connections': gate.inputs
                }
                for name, gate in self.gates.items()
            }
        }
    
    def export_to_json(self, output_file: str) -> None:
        """Export gate information to a JSON file."""
        import json
        data = self.export_to_dict()
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Exported gate information to {output_file}")


def main():
    """Example usage of the BENCH parser."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python bench_parser.py <bench_file> [output_json]")
        print("Example: python bench_parser.py circuit.bench")
        print("Example: python bench_parser.py circuit.bench output.json")
        sys.exit(1)
    
    bench_file = sys.argv[1]
    parser = BenchParser()
    
    try:
        parser.parse_file(bench_file)
        
        # Print statistics
        stats = parser.get_statistics()
        print("\n=== Circuit Statistics ===")
        print(f"Total Gates: {stats['total_gates']}")
        print(f"Total Inputs: {stats['total_inputs']}")
        print(f"Total Outputs: {stats['total_outputs']}")
        print(f"Total Nodes: {stats['total_nodes']}")
        print("\nGate Type Distribution:")
        for gate_type, count in sorted(stats['gate_type_counts'].items()):
            print(f"  {gate_type}: {count}")
        
        # Export to JSON if output file specified
        if len(sys.argv) >= 3:
            output_json = sys.argv[2]
            parser.export_to_json(output_json)
        
        # Example: Print first few gates
        print("\n=== Sample Gates (first 5) ===")
        for i, (name, gate) in enumerate(list(parser.get_all_gates().items())[:5]):
            print(f"{i+1}. {gate}")
        
    except FileNotFoundError:
        print(f"Error: File '{bench_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
