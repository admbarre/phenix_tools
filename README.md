# phenix_tools
Set of tools to more easily interact with imaging experiments carried out on Opera Phenix microscope platform.

# Usage
- Provide the top level experiment directory
- Inspect the summarized details by printing the experiment
- Inspect the general plate layout by using **get_layout()**
- Provide rules for the coating as well as the cells and other media conditions
  - NOTE: this is to be moved into a separate plate coating module
- Group files according to metadata for easier reading and pipelining into ImageJ
