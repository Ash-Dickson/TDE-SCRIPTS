import subprocess
import os
import ast
from collections import defaultdict


parent = os.getcwd()
outputs = []
for N in range(1, 51):
    os.chdir(str(N))
    result = subprocess.run(['python3', '../foldcell.py'], capture_output=True, text=True)
    if result.returncode == 0:
        outputs.append(result.stdout)
    os.chdir(parent)



sums = defaultdict(int)

# Iterate over the outputs
for output in outputs:
    # Parse the string into a dictionary
    output_dict = ast.literal_eval(output)

    # Add the values to the corresponding keys in the sums dictionary
    for key, value in output_dict.items():
        sums[key] += value

# Convert the defaultdict to a regular dictionary
sums_dict = dict(sums)

# Print the final dictionary
print(sums_dict)
