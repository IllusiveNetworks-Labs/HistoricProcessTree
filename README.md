# HistoricProcessTree
HistoricProcessTree receives a Security Event Log file (evtx)  and visualizes historic process execution evidence (based on 4688 events) in a tree view.

Analyzing processes execution, their time and their ancestors, provides researchers an initial understanding of what happened on an investigated machine.

Additional reading material on the tool, can be found in our blog [Visualising Historic Process Execution Events](https://blog.illusivenetworks.com/improving-cyber-investigation-better-visualization-of-historic-process-execution-events).

## Requirements
* Powershell
* [Python Anytree module](https://pypi.python.org/pypi/anytree)
* [Python jinja2 module](http://jinja.pocoo.org/)
```
pip install anytree jinja2
```

## How to use
```
Usage: HistoricProcessTree.py [-h] [-s START_TIME] [-e END_TIME] [--hours NUM_OF_HOURS] input_file output_file

positional arguments:
  input_file            Path to evtx file
  output_file           Final name of the generated HTML

optional arguments:
  -h, --help               Show this help message and exit
  -s START_TIME 		   Start date filter- Format: "MM/DD/YYYY HH:MM:SS"
  -e END_TIME       	   End date filter- Format: "MM/DD/YYYY HH:MM:SS"
  --hours HOURS            Number of hours to go back since last event

```
## Examples
HistoricProcessTree.py c:\work\Security.evtx -s “01/10/2018 15:45:00” -e “01/10/2017 16:00” output_file.html 
Note: Run this from the tool's working directory

will generate the following HTML page:

![alt tag](http://image.ibb.co/dK1nbw/process_tree_final.jpg "process_tree")<br /> 

## Authors

* Tom Kahana- [@tomkahana1](https://twitter.com/tomkahana1)

## License 

This project is licensed under the  BSD 3-clause license - see the [LICENSE](LICENSE) file for details

## Contributors
* [Illusive Networks](https://www.illusivenetworks.com/) Research & Dev team members:
	* Tom Sela
	* Dolev Ben Shushan
	* Hadar Yudovich
	* Yair Fried
* Jonathan Miles for JQuery Plugin bootstrap-treeview.js

