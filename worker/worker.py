import json
import pika, os
from database import insert_router_info
from netmiko import ConnectHandler

def interface_info(host, username, password):

    cisco_router = {
    'device_type': 'cisco_ios', # Multi-vendor (e.g., juniper_junos, arista_eos)
    'host': host,
    'username': username,
    'password': password,
    'secret': 'enablePassword', # Optional: For privileged mode
    'disabled_algorithms': {'pubkeys': ['rsa-sha2-256', 'rsa-sha2-512']}
    }

    ssh = ConnectHandler(**cisco_router)
    result = ssh.send_command("show ip interface brief", use_textfsm=True)
    return result

def queue_consume(host):

    username = os.environ.get("RABBITMQ_DEFAULT_USER") 
    password = os.environ.get("RABBITMQ_DEFAULT_PASS")

    # Set your username and password
    credentials = pika.PlainCredentials(username, password)

    # Set up connection parameters (host, port, virtual_host, credentials)
    parameters = pika.ConnectionParameters(
        host=host, port=5672, virtual_host="/", credentials=credentials, connection_attempts=3,retry_delay=2
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='router_jobs')

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        info = interface_info(data['ip'], data['username'], data['password'])
        print(info)
        insert_router_info(data['ip'], info)

    channel.basic_consume(queue='router_jobs', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages.')

    channel.start_consuming()
    
if __name__ == "__main__":
    target = os.environ.get("TARGET_QUEUE")
    queue_consume(target)