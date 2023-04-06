import speedtest
import statistics
import matplotlib.pyplot as plt
import csv
import json

class SpeedTest:
    def __init__(self):
        self.st = speedtest.Speedtest()
        print("Loading server list...")
        self.st.get_servers()

    def choose_best_server(self):
        print("Testing servers...")
        self.servers = self.st.get_servers()
        self.best_server = None
        for server in self.servers:
            if server is None or not isinstance(server, dict) or 'url' not in server:
                continue
            server_id = server['id']
            server_country = server['country']
            print(f"Testing server {server_id} located in {server_country}...")
            self.st.get_best_server([server])
            download_speed = self.st.download() / 1024 / 1024
            print(f"Download speed: {download_speed:.2f} Mbit/s")
            if self.best_server is None or download_speed > self.best_server['download_speed']:
                self.best_server = {
                    "host": server['host'],
                    "country": server_country,
                    "download_speed": download_speed
                }
        if self.best_server is not None:
            print(f"Best server: {self.best_server['host']} located in {self.best_server['country']}")

    def run_tests(self, num_tests):
        self.choose_best_server()
        download_speeds = []
        upload_speeds = []
        ping_times = []
        latencies = []
        jitters = []
        packet_losses = []
        results = []
        for i in range(num_tests):
            print(f"Test {i+1}")
            if self.best_server is not None:
                self.st.get_best_server([self.best_server])
                
                download_speed = self.st.download() / 1024 / 1024
                upload_speed = self.st.upload() / 1024 / 1024
                ping = self.st.results.ping
                latency = self.st.results.server.get('latency')
                jitter = self.st.results.server.get('jitter')
                packet_loss = self.st.results.packet_loss
                
                print(f"Download speed: {download_speed:.2f} Mbit/s")
                print(f"Upload speed: {upload_speed:.2f} Mbit/s")
                print(f"Ping time: {ping:.2f} ms")
                print(f"Latency: {latency:.2f} ms")
                print(f"Jitter: {jitter:.2f} ms")
                print(f"Packet loss: {packet_loss:.2f} %")
                
                download_speeds.append(download_speed)
                upload_speeds.append(upload_speed)
                ping_times.append(ping)
                latencies.append(latency)
                jitters.append(jitter)
                packet_losses.append(packet_loss)
                results.append({
                    "test_number": i + 1,
                    "download_speed": download_speed,
                    "upload_speed": upload_speed,
                    "ping_time": ping,
                    "latency": latency,
                    "jitter": jitter,
                    "packet_loss": packet_loss
                })

        self.avg_download_speed = sum(download_speeds) / num_tests
        self.avg_upload_speed = sum(upload_speeds) / num_tests
        self.avg_ping_time = sum(ping_times) / num_tests
        self.avg_latency = sum(latencies) / num_tests
        self.avg_jitter = sum(jitters) / num_tests
        self.avg_packet_loss = sum(packet_losses) / num_tests
        self.results = results # Add this line to assign the results to instance attribute

        self.plot_results(download_speeds, upload_speeds)
        self.save_results(results)


    def plot_results(self, download_speeds, upload_speeds):
        plt.plot(download_speeds, label='Download Speed')
        plt.plot(upload_speeds, label='Upload Speed')
        plt.title('Internet Speed Test Results')
        plt.xlabel('Test Number')
        plt.ylabel('Speed (Mbps)')
        plt.legend()
        plt.show()

    def save_results(self, results, output_file=None):
        if output_file:
            extension = output_file.split(".")[-1].lower()
            if extension == "csv":
                with open(output_file, mode="w", newline="") as file:
                    fieldnames = ["test_number", "download_speed", "upload_speed", "ping_time"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    for result in results:
                        writer.writerow(result)
            elif extension == "json":
                with open(output_file, mode="w") as file:
                    json.dump(results, file)

    def print_results(self):
        download_speeds_stddev = None
        if len(self.results) > 1:
            download_speeds_stddev = statistics.stdev(self.results[i]['download_speed'] for i in range(len(self.results)))
        print("Results:")
        print(f"  Download speed (average): {self.avg_download_speed:.2f} Mbit/s")
        if download_speeds_stddev is not None:
            print(f"  Download speed (standard deviation): {download_speeds_stddev:.2f} Mbit/s")
        else:
            print("  Download speed (standard deviation): Not enough data")
        print(f"  Upload speed (average): {self.avg_upload_speed:.2f} Mbit/s")
        print(f"  Ping time (average): {self.avg_ping_time:.2f} ms")
        print(f"  Latency (average): {self.avg_latency:.2f} ms")
        print(f"  Jitter (average): {self.avg_jitter:.2f} ms")
        print(f"  Packet loss (average): {self.avg_packet_loss:.2f} %")


def test_speed(num_tests, output_file=None):
    speed_test = SpeedTest()
    speed_test.run_tests(num_tests)
    speed_test.print_results()
    speed_test.save_results(speed_test.results, output_file)


# Example usage: run 5 tests, average the results, and save them to a CSV file
test_speed(5, "speed_test_results.csv")

# Example usage: run 10 tests, average the results, and save them to a JSON file
test_speed(10, "speed_test_results.json")






