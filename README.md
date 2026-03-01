# BENCH Format Parser

A high-performance Python parser for BENCH format files that can handle large circuits (up to 500k+ lines).

## Features

- Parses BENCH format netlists efficiently
- Handles both syntax formats:
  - `GATE_TYPE(output, input1, input2, ...)` 
  - `output = GATE_TYPE(input1, input2, ...)`
- Stores gate information:
  - Gate type (AND, OR, NAND, NOR, XOR, XNOR, NOT, etc.)
  - Gate name (output wire/node)
  - Connections (which nodes connect to this gate's inputs)
- Memory efficient for large files
- Progress reporting for large files

## Usage

### Command Line

```bash
# Basic usage
python3 bench_parser.py circuit.bench

# Export to JSON
python3 bench_parser.py circuit.bench output.json
```

### Programmatic Usage

```python
from bench_parser import BenchParser

# Create parser
parser = BenchParser()

# Parse file
parser.parse_file('circuit.bench')

# Get specific gate information
gate_info = parser.get_gate_info('gate_name')
# Returns: {'gate_type': 'AND', 'gate_name': 'gate_name', 'connections': ['input1', 'input2']}

# Get all gates
all_gates = parser.get_all_gates()

# Get connections for a gate
connections = parser.get_connections('gate_name')

# Find gates by type
and_gates = parser.find_gates_by_type('AND')

# Get statistics
stats = parser.get_statistics()

# Export to JSON
parser.export_to_json('output.json')
```

## Gate Information Structure

For each gate, the parser stores:
1. **Gate Type**: The type of gate (AND, OR, NAND, NOR, XOR, XNOR, NOT, etc.)
2. **Gate Name**: The output wire/node name
3. **Connections**: List of input node names that connect to this gate

## Example

Given a BENCH file:
```
INPUT(A)
INPUT(B)
OUTPUT(Sum)
AND(A1, A, B)
XOR(Sum, A1, B)
```

The parser will extract:
- Gate `A1`: Type=AND, Connections=[A, B]
- Gate `Sum`: Type=XOR, Connections=[A1, B]

## Performance

The parser is optimized for large files:
- Processes files line by line (memory efficient)
- Progress reporting every 50,000 lines
- Efficient data structures for fast lookups

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)
