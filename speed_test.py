import speedtest
from tabulate import tabulate
import json
import csv
import numpy as np
import statistics
import matplotlib.pyplot as plt


class SpeedTest:
    def __init__(self):
        self.st = speedtest.Speedtest()
        self.results = None
    
    def load_results(self, file_path):
        try:
            with open(file_path, 'r') as f:
                self.results = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading results from {file_path}: {e}")
            return

    def run_tests(self, num_tests):
        print("Loading server list...")
        try:
            self.st.get_servers()
        except speedtest.SpeedtestException as e:
            print(f"Error loading server list: {e}")
            return

        print("Choosing best server...")
        try:
            best_server = self.st.get_best_server()
        except speedtest.SpeedtestException as e:
            print(f"Error choosing best server: {e}")
            return
        print(f"Found: {best_server['host']} located in {best_server['country']}")

        print(f"Performing {num_tests} tests...")
        download_speeds = []
        upload_speeds = []
        ping_times = []
        for i in range(num_tests):
            print(f"Test {i+1}")
            try:
                download_speed = self.st.download() / 1024 / 1024
                upload_speed = self.st.upload() / 1024 / 1024
                ping = self.st.results.ping
            except speedtest.SpeedtestException as e:
                print(f"Error during test {i+1}: {e}")
                return

            print(f"Download speed: {download_speed:.2f} Mbit/s")
            print(f"Upload speed: {upload_speed:.2f} Mbit/s")
            print(f"Ping: {ping:.2f} ms")
            download_speeds.append(download_speed)
            upload_speeds.append(upload_speed)
            ping_times.append(ping)

        self.results = {
            "download_speeds": download_speeds,
            "upload_speeds": upload_speeds,
            "ping_times": ping_times,
        }

    def print_results(self):
        if self.results is None:
            print("No results to print")
            return

        download_speeds = self.results["download_speeds"]
        upload_speeds = self.results["upload_speeds"]
        ping_times = self.results["ping_times"]
        num_tests = len(download_speeds)

        avg_download_speed = sum(download_speeds) / num_tests
        avg_upload_speed = sum(upload_speeds) / num_tests
        avg_ping_time = sum(ping_times) / num_tests
        std_download_speed = statistics.stdev(download_speeds)
        std_upload_speed = statistics.stdev(upload_speeds)
        max_download_speed = max(download_speeds)
        min_download_speed = min(download_speeds)
        max_upload_speed = max(upload_speeds)
        min_upload_speed = min(upload_speeds)
        median_download_speed = statistics.median(download_speeds)
        median_upload_speed = statistics.median(upload_speeds)
        mode_ping_time = statistics.mode(ping_times)

        table = [
            ['Average download speed', f"{avg_download_speed:.2f} Mbit/s"],
            ['Median download speed', f"{median_download_speed:.2f} Mbit/s"],
            ['Standard deviation of download speed', f"{std_download_speed:.2f}"],
            ['Maximum download speed', f"{max_download_speed:.2f} Mbit/s"],
            ['Minimum download speed', f"{min_download_speed:.2f} Mbit/s"],
            ['Average upload speed', f"{avg_upload_speed:.2f} Mbit/s"],
            ['Median upload speed', f"{median_upload_speed:.2f} Mbit/s"],
            ['Standard deviation of upload speed', f"{std_upload_speed:.2f}"],
            ['Maximum upload speed', f"{max_upload_speed:.2f} Mbit/s"],
            ['Minimum upload speed', f"{min_upload_speed:.2f} Mbit/s"],
            ['Average ping time', f"{avg_ping_time:.2f} ms"],
            ['Mode of ping times', f"{mode_ping_time:.2f} ms"],
        ]

        print(tabulate(table, headers=['Metric', 'Value'], tablefmt='orgtbl'))



    def plot_results(self):
        if self.results is None:
            print("No results to plot")
            return

        download_speeds = self.results["download_speeds"]
        upload_speeds = self.results["upload_speeds"]
        num_tests = len(download_speeds)

        plt.plot(download_speeds, label='Download Speed')
        plt.plot(upload_speeds, label='Upload Speed')
        plt.title('Internet Speed Test Results')
        plt.xlabel('Test Number')
        plt.ylabel('Speed (Mbps)')
        plt.legend()
        plt.show()

        ping_times = self.results["ping_times"]
        plt.figure()
        plt.hist(ping_times, bins=10)
        plt.title('Ping Time Distribution')
        plt.xlabel('Ping Time (ms)')
        plt.ylabel('Frequency')
        plt.show()

    def save_results(self, file_path, format='json'):
        if self.results is None:
            print("No results to save")
            return

        if format == 'json':
            with open(file_path, 'w') as f:
                json.dump(self.results, f)
        elif format == 'csv':
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Download Speed (Mbit/s)', 'Upload Speed (Mbit/s)', 'Ping Time (ms)'])
                for i in range(len(self.results['download_speeds'])):
                    writer.writerow([self.results['download_speeds'][i], self.results['upload_speeds'][i], self.results['ping_times'][i]])
        else:
            print(f"Unsupported format: {format}")

    def display_previous_results(self):
        if self.results is None:
            print("No previous results to display")
            return

        print("Previous test results:")
        download_speeds = self.results["download_speeds"]
        upload_speeds = self.results["upload_speeds"]
        ping_times = self.results["ping_times"]
        num_tests = len(download_speeds)

        for i in range(num_tests):
            print(f"Test {i+1}")
            print(f"Download speed: {download_speeds[i]:.2f} Mbit/s")
            print(f"Upload speed: {upload_speeds[i]:.2f} Mbit/s")
            print(f"Ping: {ping_times[i]:.2f} ms")

def test_speed(num_tests):
    speed_test = SpeedTest()
    speed_test.run_tests(5)
    # speed_test.load_results("previous_results.json") 
    # or speed_test.display_previous_results() to display the previous test results.
    speed_test.print_results()
    speed_test.plot_results()
    speed_test.save_results('results.json') # save results to a JSON file
    speed_test.save_results('results.csv', 'csv') # save results to a CSV file

# Example usage: run 5 tests and average the results
test_speed(5)






