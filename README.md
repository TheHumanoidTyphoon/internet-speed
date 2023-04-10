# Internet Speed Test

This Python script measures your internet speed by performing a series of download, upload, and ping tests using the speedtest library. The results are displayed as a table of metrics, such as average download speed, median upload speed, and standard deviation of ping times. Additionally, the results can be plotted in a line chart and a histogram. The results can be saved in either JSON or CSV format for later analysis.

## Installation
Clone the repository or download the files.
Install the required Python packages: 
- `speedtest` 
- `tabulate` 
- `json`
- `csv` 
- `numpy` 
- `statistics` 
- `matplotlib`
## Usage
To run the script, navigate to the directory where the files are saved and type the following command in your terminal:
```python
python speed_test.py
```
### Commands
The script has the following commands:
- `load_results(file_path)`: loads previous test results from a `JSON` file.
- `run_tests(num_tests)`: runs a series of internet speed tests and generates metrics and visualizations.
- `print_results()`: prints the metrics generated from the most recent test.
- `plot_results()`: generates plots of the download and upload speeds and the ping times.
- `save_results(file_path, format)`: saves the results of the most recent test to a `JSON` or `CSV` file.
## Example
Here's an example of how to use the script:
```python
speed_test = SpeedTest()
speed_test.load_results('results.json')
speed_test.run_tests(3)
speed_test.print_results()
speed_test.plot_results()
speed_test.save_results('results.csv', format='csv')
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/TheHumanoidTyphoon/internet-speed/blob/master/LICENSE) file for details.
