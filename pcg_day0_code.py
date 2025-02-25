
import yaml
import re

def read_input_from_file(file_path):
    """
    Read the input data from a file and return it as a list of values.
    Each line in the file corresponds to a specific input value.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Clean up any extra whitespace or newline characters
    return [line.strip() for line in lines]

def generate_updates(values):
    """
    Generate the updates dictionary dynamically based on the values read from the file.
    """
    return {
        'global': {
            'ericsson': {
                'licensing': {
                    'licenseDomains': [
                        {
                            'productType': values[0],    # PACKET_CORE_CONTROLLER
                            'customerId': values[1],     # 940157
                            'swltId': values[2]          # BHARTI_PCC-SM_00
                        }
                    ]
                }
            }
        },
        'global': {
            'licensing': {
                    'sites': [
                        {
                                'hostname': values[3],            # 2401:4900:0024:0506::10
                                'ip': values[4],            # 6514                                
                        },
                        {
                                'hostname': values[5],           # 2401:4900:90:1000::9c7
                                'ip': values[6],           # 514
                        }
                ]
            }
        },

        'eric-cloud-native-base': {
            'eric-fh-snmp-alarm-provider': {
                'service': {
                    'externalIPv6': {
                        'loadBalancerIP': values[7]  # 2401:4900:90:1000::9c3
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
                                'host': values[8],            # 2401:4900:0024:0506::10
                                'port': values[9],            # 6514    
                            },
                            {
                                'host': values[10],           # 2401:4900:90:1000::9c7
                                'port': values[11],           # 514
                            }
                        ]
                    }
                }
            }
        }
    }

def update_yaml(yaml_file_path, updates):
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
    
    deep_update(data, updates)

    # Save the updated YAML file
    with open(yaml_file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

# Specify the YAML file path and the input data file path
yaml_file_path = 'pcg_values.yaml'
input_file_path = 'pcg_input_file.txt'  # File containing the dynamic input values

# Read input values from the text file
input_values = read_input_from_file(input_file_path)

# Generate the updates dictionary based on the input values
updates = generate_updates(input_values)

# Update the YAML file with the dynamic updates
update_yaml(yaml_file_path, updates)

print(f"YAML file {yaml_file_path} has been updated successfully.")
