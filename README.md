# phenix_tools
Set of tools to more easily interact with imaging experiments carried out on Opera Phenix microscope platform.

# Usage (import module into Jupyter Notebook)
- Provide the top level experiment directory
- Inspect the summarized details by printing the experiment
<img width="563" alt="sumary" src="https://github.com/admbarre/phenix_tools/assets/7918190/51dd6b6e-a63c-4791-9d5d-db18e68f6af9">

- Inspect the general plate layout by using **get_layout()**
<img width="720" alt="layout" src="https://github.com/admbarre/phenix_tools/assets/7918190/efa04340-3c31-41d9-86b8-d280807be096">

- Provide rules for the coating as well as the cells and other media conditions
  - NOTE: this is to be moved into a separate plate coating module
<img width="455" alt="gfp rules" src="https://github.com/admbarre/phenix_tools/assets/7918190/e72cf4ea-c605-49dd-9e77-446c25a203cf">
<hr>
<img width="320" alt="cell rules" src="https://github.com/admbarre/phenix_tools/assets/7918190/c0caec7e-52f6-4cab-aa9b-5fb0f2646b55">

- Group files according to metadata for easier reading and pipelining into ImageJ

![usage_AdobeExpress](https://github.com/admbarre/phenix_tools/assets/7918190/0d059230-6904-422d-9338-20e1f7d2d9e1)
