from flask import Flask, render_template, request
from netmiko import ConnectHandler

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    error = None
    success = False

    router_device = {
        "device_type": "cisco_ios_telnet",
        "ip": "192.168.10.37",
        "port": 32770,
        "username": "admin",
        "password": "eve123",
        "secret": "eve123",
    }

    # Changed from a list to a dictionary so commands.items() works in HTML
    commands_to_run = {
        "version": "show version",
        "interfaces": "show ip interface brief",
        "config": "show running-config",
    }

    if request.method == "POST":
        net_connect = None
        try:
            net_connect = ConnectHandler(**router_device)
            net_connect.enable()

            # Loop through dictionary values to run each command
            for key, cmd in commands_to_run.items():
                output = net_connect.send_command(cmd)
                results[cmd] = output

            success = True

        except Exception as e:
            error = f"Connection failed: {str(e)}"

        finally:
            if net_connect:
                net_connect.disconnect()

    return render_template(
        "index.html",
        results=results,
        error=error,
        success=success,
        router_ip=router_device["ip"],
        router_port=router_device["port"],
        commands=commands_to_run,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
