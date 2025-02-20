import yaml
import re
# Define the mapping from the Day0filechanges.txt data
updates = {
    'global': {
        'ericsson': {
            'licensing': {
                'licenseDomains': [
                    {
                        'productType': 'PACKET_CORE_CONTROLLER',
                        'customerId': '940157',
                        'swltId': 'BHARTI_PCC-SM_00'
                    }
                ]
            }
        },
        'timezone': 'Asia/Kolkata',  # Update Timezone
        'applicationId': 'MPGVPRHCK01ERPCCSM01',  # Update Application ID
    },

    'eric-pc-sm': {
        'eric-pc-sm-notification-forwarder': {
            'services': {
                'namfnotification-ipv6': {
                    'annotations': {
                        'metallb.universe.tf/address-pool': 'smf-nsmf-service',
                        'metallb.universe.tf/allow-shared-ip': 'smf-nsmf-service'
                    }
                }
            }
        }
    },
	
    'eric-cloud-native-base': {
        'eric-tm-ingress-controller-cr': {
            'service': {
                'externalIPv6': {
                    'loadBalancerIP': '2401:4900:90:1000::9c3'
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
                                'host': '2401:4900:0024:0506::10',
                                'port': '6514',
                                'sourcehost': 'MPGVPRHCK01ERPCCSM01'
                            },
                            {
                                'host': '2401:4900:90:1000::9c7',
                                'port': '514',
                                'sourcehost': 'MPGVPRHCK01ERPCCSM01'
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

# Specify your YAML file path
yaml_file_path = 'your_config_file.yaml'

# Update the YAML file
update_yaml(yaml_file_path, updates)

print(f"YAML file {yaml_file_path} has been updated successfully.")
