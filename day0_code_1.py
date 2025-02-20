import yaml

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
    },
    'applicationId': 'MPGVPRHCK01ERPCCSM01',  # Update Application ID
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
