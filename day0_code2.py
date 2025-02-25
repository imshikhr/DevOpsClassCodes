import yaml
import re

# Define the mapping from the Day0filechanges.txt data (for updating specific values)
updates = {
    'global': {
        'ericsson': {
            'licensing': {
                'licenseDomains': [
                    {
                        'productType': '',  # placeholder
                        'customerId': '',   # placeholder
                        'swltId': ''        # placeholder
                    }
                ]
            }
        },
        'timezone': 'Asia/Kolkata',  # Update Timezone
        'applicationId': '',  # Update Application ID
    },
    'eric-pc-sm': {
        'eric-pc-sm-notification-forwarder': {
            'services': {
                'namfnotification-ipv6': {
                    'annotations': {
                        'metallb.universe.tf/address-pool': '',
                        'metallb.universe.tf/allow-shared-ip': ''
                    }
                }
            }
        }
    },
    'eric-cloud-native-base': {
        'eric-tm-ingress-controller-cr': {
            'service': {
                'externalIPv6': {
                    'loadBalancerIP': ''
                }
            }
        }
    },
    'eric-cloud-native-base': {
        'eric-log-transformer': {
            'egress': {
                'syslog': {
                    'remoteHosts': [
                        {
                            'host': '',
                            'port': '',
                            'sourcehost': ''
                        },
                        {
                            'host': '',
                            'port': '',
                            'sourcehost': ''
                        }
                    ]
                }
            }
        }
    }
}    

def read_updates_from_file(file_path):
    """
    Read the text file and return a dictionary with mapped key-value pairs.
    Each line corresponds to a value to be updated in the YAML structure.
    """
    updates_from_file = [
        "global.ericsson.licensing.licenseDomains.0.productType",  # Placeholder key
        "global.ericsson.licensing.licenseDomains.0.customerId",   # Placeholder key
        "global.ericsson.licensing.licenseDomains.0.swltId",        # Placeholder key
        "global.applicationId", # Placeholder key
        "eric-pc-sm.eric-pc-sm-notification-forwarder.services.smf-nsmf-service.annotations.metallb.universe.tf/address-pool",  # Placeholder key
        "eric-pc-sm.eric-pc-sm-notification-forwarder.services.smf-nsmf-service.annotations.metallb.universe.tf/allow-shared-ip",  # Placeholder key
        "eric-cloud-native-base.eric-tm-ingress-controller-cr.service.externalIPv6.loadBalancerIP",  # Placeholder key
        "eric-cloud-native-base.eric-log-transformer.egress.syslog.remoteHosts.0.host",  # Placeholder key
        "eric-cloud-native-base.eric-log-transformer.egress.syslog.remoteHosts.0.port",
        "eric-cloud-native-base.eric-log-transformer.egress.syslog.remoteHosts.0.sourcehost",  # Placeholder key
        "eric-cloud-native-base.eric-log-transformer.egress.syslog.remoteHosts.1.host",  # Placeholder key
        "eric-cloud-native-base.eric-log-transformer.egress.syslog.remoteHosts.1.port",
        "eric-cloud-native-base.eric-log-transformer.egress.syslog.remoteHosts.1.sourcehost",  # Placeholder key
    ]
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # This list corresponds to the positions where the values will be inserted
    values = [
        lines[0].strip(),  # PACKET_CORE_CONTROLLER
        lines[1].strip(),  # 940157 (customerId)
        lines[2].strip(),  # BHARTI_PCC-SM_00 (swltId)
        lines[3].strip(),  # MPGVPRHCK01ERPCCSM01 (applicationId)
        lines[4].strip(),  # smf-nsmf-service (address-pool)
        lines[5].strip(),  # smf-nsmf-service (allow-shared-ip)
        lines[6].strip(),  # loadbalancer IP (loadbalancer ip)
        lines[7].strip(),  # 2401:4900:90:1000::9c3 (host)
        lines[8].strip(),  # 2401:4900:0024:0506::10 (sourcehost)
        lines[9].strip(),  # 6514 (port)
        lines[10].strip(),  # MPGVPRHCK01ERPCCSM01 (host for 2nd entry)
        lines[11].strip(),  # 2401:4900:90:1000::9c7 (host)
        lines[12].strip(),  # 514 (port)
    ]
    
    # Map values to the keys
    updates_dict = {}
    for key, value in zip(updates_from_file, values):
        keys = key.split('.')
        current = updates_dict
        for part in keys[:-1]:
            current = current.setdefault(part, {})
        current[keys[-1]] = value
    
    return updates_dict

def update_yaml(yaml_file_path, updates, updates_from_file):
    # Load the existing YAML file
    with open(yaml_file_path, 'r') as f:
        data = yaml.safe_load(f)

    # Update the YAML data based on the provided dictionary
    def deep_update(d, u):
        for k, v in u.items():
            if isinstance(v, dict) and k in d:
                deep_update(d[k], v)
            else:
                d[k] = v
    
    # Apply the updates from the provided text file to the original updates first
    deep_update(updates, updates_from_file)

    # Update the YAML file with the final updates
    deep_update(data, updates)

    # Save the updated YAML file
    with open(yaml_file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

# Specify your YAML file path and the text file path for updates
yaml_file_path = 'your_config_file.yaml'
text_file_path = 'Day0filechanges.txt'  # File containing the values

# Read updates from the text file
updates_from_file = read_updates_from_file(text_file_path)

# Update the YAML file
update_yaml(yaml_file_path, updates, updates_from_file)

print(f"YAML file {yaml_file_path} has been updated successfully.")
