import speedtest

def test_speed():
    st = speedtest.Speedtest()
    print("Loading server list...")
    st.get_servers()
    print("Choosing best server...")
    best_server = st.get_best_server()
    print(f"Found: {best_server['host']} located in {best_server['country']}")

    print("Performing download, upload and ping tests...")
    download_speed = st.download() / 1024 / 1024
    upload_speed = st.upload() / 1024 / 1024
    ping = st.results.ping

    print(f"Download speed: {download_speed:.2f} Mbit/s")
    print(f"Upload speed: {upload_speed:.2f} Mbit/s")
    print(f"Ping: {ping:.2f} ms")

test_speed()


