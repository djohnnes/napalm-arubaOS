import paramiko
import time

"""
A generic and agnostic module to establish SSH connection to any devices that supports SSH.
"""


def ssh_connector(hostname, username, password, key=False, timeout=10, port=22):
    """ Connect to remote device and return a channel to use for sending cmds.
        return the returned value is the channel object that will be used to send command to remote device
    """
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username,
                    password=password, look_for_keys=key, timeout=timeout)
        print("Connected to {0}\n".format(hostname))
    except:
        print("Could not connect to {0}".format(hostname))
        ssh.close()
        return None
    else:
        channel = ssh.invoke_shell()
        return channel


def send_single_cmd(cmd, channel, incoming_sleep_time=2, out_going_sleep_time=2):
    """Send cmd via the channel if channel object is not None
        return: the return value is the result or the executed cmd
    """
    if not cmd:
        print(f"Not command to send\n")
        return None
    if not channel:
        print(f"No channel available\n")
        return None

    banner = channel.recv(99999).decode("utf-8")
    time.sleep(1)
    print(f"{banner}\n\n")
    time.sleep(1)

    channel.send(cmd + "\n")
    time.sleep(out_going_sleep_time)

    output = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    return output

