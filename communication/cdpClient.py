from cdp_client import cdp

def on_value_changed(value, timestamp):
    print(value)

def subscribe_to_value_changes(node):
    node.subscribe_to_value_changes(on_value_changed)

client = cdp.Client('127.0.0.1')
client.find_node('AppName.ComponentName.SignalName').then(subscribe_to_value_changes)
client.run_event_loop()