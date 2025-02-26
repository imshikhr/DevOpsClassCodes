import yaml
import re

# Define the mapping from the Day0filechanges.txt data (for updating specific values)
updates = {
    'global': {
        'ericsson': {
            'licensing': {
                'licenseDomains': [
                    {
                        'productType': 
                        'customerId':
                        'swltId':
                    }
                ]
            },
            'licensing': {
                'sites': [
                    {
                        'hostname':
                        'ip':
                    },
                    {
                        'hostname':
                        'ip':
                    }
                ]
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
        "global.licensing.sites[0].hostname",  # Placeholder key
        "global.licensing.sites[0].ip",   # Placeholder key
        "global.licensing.sites[1].hostname",  # Placeholder key
        "global.licensing.sites[1].ip"
    ]
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # This list corresponds to the positions where the values will be inserted
    values = [
        str(lines[0].strip()),  # PACKET_CORE_CONTROLLER
        str(lines[1].strip()),  # 940157 (customerId)
        str(lines[2].strip()),  # BHARTI_PCC-SM_00 (swltId)
        str(lines[3].strip()),  # MPGVPRHCK01ERPCCSM01 (applicationId)
        str(lines[4].strip()),  # smf-nsmf-service (address-pool)
        str(lines[5].strip()),  # smf-nsmf-service (allow-shared-ip)
        str(lines[6].strip()),  # loadbalancer IP (loadbalancer ip)
    ]
    
    # Map values to the keys
    updates_dict = {}
    for key, value in zip(updates_from_file, values):
        keys = key.split('.')
        current = updates_dict
        for part in keys[:-1]:
            if '[' in part:  # Handling list indices in the key
                list_index = int(re.search(r'\[(\d+)\]', part).group(1))  # Extract index from [index]
                list_part = part.split('[')[0]
                current = current.setdefault(list_part, [])[list_index]
            else:
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
yaml_file_path = 'pcg_values.yaml'
text_file_path = 'pcg_test.txt'  # File containing the values

# Read updates from the text file
updates_from_file = read_updates_from_file(text_file_path)

# Update the YAML file
update_yaml(yaml_file_path, updates, updates_from_file)

print(f"YAML file {yaml_file_path} has been updated successfully.")
