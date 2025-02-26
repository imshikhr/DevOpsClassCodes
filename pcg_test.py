import yaml

def read_input_from_file(file_path):
    """
    Read the input data from a file and return it as a list of values.
    Each line in the file corresponds to a specific input value.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Clean up any extra whitespace or newline characters
    return [line.strip().strip('"') for line in lines]

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
                            'productType': values[0],    # PACKET_CORE_GATEWAY
                            'customerId': values[1],     # 940157
                            'swltId': values[2]          # BHARTI_PCG-UP_00
                        }
                    ]
                }
            },
            'timezone': 'Asia/Kolkata',  # Static value
            'nodeSelector': {
                'eric-pod': 'paco'
            },
            'pcfw': {
                'enabled': False
            }
        },

        'licensing': {
            'sites': [
                {
                    'hostname': values[3],            # uppal.nels
                    'ip': values[4],                  # 2401:4900:d4:1600::0a14
                    'priority': 30
                },
                {
                    'hostname': values[5],            # vijaywada.nels
                    'ip': values[6],                  # 2401:4900:d4:1700::05ee
                    'priority': 50
                }
            ]
        },

        'eric-tm-partition-distributor': {
            'enabled': True,
            'replicaCount': 5,
            'resources': {
                'partitionDistributor': {
                    'limits': {
                        'cpu': 1,
                        'memory': '512Mi'
                    },
                    'requests': {
                        'cpu': 0.2,
                        'memory': '0.1Gi'
                    }
                }
            }
        },

        'eric-pc-up-data-plane': {
            'enabled': True,
            'allowNetworkConfigChanges': False,
            'deployment': {
                'pinThreads': True
            },
            'acceleratedIo': {
                'driver': 'bifurcated',
                'enabled': True,
                'pciDeviceArguments': [
                    'rxq_cqe_comp_en=0'
                ]
            },
            'replicaCount': 72,
            'resources': {
                'dataPlane': {
                    'requests': {
                        'openshift.io/sriovleftmellanox': 1,
                        'openshift.io/sriovrightmellanox': 1,
                        'hugepages-1Gi': '2Gi',
                        'cpu': 16,
                        'memory': '12Gi'
                    },
                    'limits': {
                        'openshift.io/sriovleftmellanox': 1,
                        'openshift.io/sriovrightmellanox': 1,
                        'hugepages-1Gi': '2Gi',
                        'cpu': 16,
                        'memory': '12Gi'
                    }
                }
            },
            'sidecar': {
                'at': False
            },
            'podDisruptionBudget': {
                'maxUnavailable': 6
            },
            'interfaces': [
                {
                    'name': 'net1',
                    'type': 'host-device',
                    'networkAttachmentDefinition': False
                },
                {
                    'name': 'net2',
                    'type': 'host-device',
                    'networkAttachmentDefinition': False
                }
            ]
        }
    }

def deep_update(d, u):
    """
    Recursively update the dictionary `d` with the dictionary `u`.
    """
    for k, v in u.items():
        if isinstance(v, dict) and k in d:
            deep_update(d[k], v)
        else:
            d[k] = v

def update_yaml(yaml_file_path, updates):
    # Load the existing YAML file
    with open(yaml_file_path, 'r') as f:
        data = yaml.safe_load(f)

    # Apply updates
    deep_update(data, updates)

    # Save the updated YAML file
    with open(yaml_file_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)

# Specify the YAML file path and the input data file path
yaml_file_path = 'pcg_values.yaml'
input_file_path = 'pcg_test.txt'  # File containing the dynamic input values

# Read input values from the text file
input_values = read_input_from_file(input_file_path)

# Generate the updates dictionary based on the input values
updates = generate_updates(input_values)

# Update the YAML file with the dynamic updates
update_yaml(yaml_file_path, updates)

print(f"YAML file {yaml_file_path} has been updated successfully.")
