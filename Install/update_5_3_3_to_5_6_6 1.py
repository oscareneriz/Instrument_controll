import json
import os
import shutil
import subprocess


def backup_overlays():
    overlay_directory = "/home/dnascript/Documents/overlay_configuration"
    backup_directory = "/home/dnascript/Documents/overlay_configuration_5_3_3"
    try:
        shutil.copytree(overlay_directory, backup_directory)
    except:
        print("Already backup of 5.3.3 created before, skipping htis step.")
    print("The backup was performed correctly!")

def update_sw_icsgui_fw():
    
    downloads_path = "/home/Downloads"
    
    #get the current directory
    current_path = os.getcwd()
    files = os.listdir(current_path)
    
    #find name of files to update
    instrument_sw_update_file = [file for file in files if 'Software' in file][0]
    icsgui_update_file =  [file for file in files if 'ICSGUI' in file][0]

    if instrument_sw_update_file:
        safe_copy_file(instrument_sw_update_file, current_path, downloads_path)
    else:
        print("No update file found.")

    if icsgui_update_file:
        safe_copy_file(icsgui_update_file, current_path, downloads_path)
    else:
        print("No ICSGUI update file found.")
    
    #run the updates
    file_paths = [
        os.path.join(downloads_path, instrument_sw_update_file), 
        os.path.join(downloads_path,icsgui_update_file)
    ]
    
    # Function to install .deb packages
    install_packages(file_paths)
    icsgui_version = get_app_version("ICSGUI.exe")
    instrument_version = get_app_version("instrument_controller")
    print(f"Version installed:\n"
      f"instrument:   {instrument_version}\n"
      f"ICSGUI:   {icsgui_version}")
    
    #run the the fw script to install all the fw of the latest sw
    print("Updating FW for current instrument build")
    ufw_path = "/usr/local/bin/ufw/update_fw.py"
    subprocess.run(['python3', ufw_path, 'ufw -nc'])
    
    #Ensure that there are only the 4 files needed in overlay_config
    entries_path = "/home/dnascript/Documents/overlay_configuration"
    files_overlay = os.listdir(entries_path)    # Get all entries in the directory specified
    # Print each entry
    for entry in files_overlay:
        print(entry)
    
    #Check if the four overlay configs are okay
    overlay_files_needed = ["NamedLocation.json","plate_handler.json","PlateHandlerNamedLocation.json","console_client.json"]
    if sorted(files_overlay) == sorted(overlay_files_needed):
        print("All the files in overlay _configuration are correct")
        for file in files_overlay:
            print(file)
    else:
        # Determine what is extra or missing for more detailed feedback
        extra_files = set(files_overlay) - set(overlay_files_needed)
        missing_files = set(overlay_files_needed) - set(files_overlay)
        
        if extra_files:
            print("Extra files found:", ", ".join(extra_files))
            for file in extra_files:
                remove_file_path = os.path.join(entries_path, file)
                try:
                    os.remove(remove_file_path)
                    print("File removed successfully")
                except Exception as e:
                    print(f"Failed to remove file: {e}")
        if missing_files:
            print("Missing files:", ", ".join(missing_files))
    
    
def safe_copy_file(source_filename, source_directory, destination_directory):
    source_file_path = os.path.join(source_directory, source_filename)
    if os.path.isfile(source_file_path):  # Make sure the file exists
        # Construct the full destination file path
        destination_file_path = os.path.join(destination_directory, source_filename)
        # Copy the file
        shutil.copyfile(source_file_path, destination_file_path)
        print(f"Successfully copied {source_filename} to {destination_directory}.")
    else:
        print(f"No file found to copy: {source_filename}")


def install_packages(files_paths):
    for file in files_paths:
        try:
            # Run dpkg to install the .deb package
            result = subprocess.run(['sudo', 'dpkg', '--install', file], check=True)
            print(f"Package {file} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {file}: {e}\nOutput:\n{e.stderr}")

def get_app_version(app_command):
    try:
        # Run the command to get the application version
        result = subprocess.run([app_command, '--version'], check=True, stdout=subprocess.PIPE)
        # Print the output, which includes the version information
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to get version for {app_command}: {e}")

def remove_empty_elements(d):
    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}


def clean_dictionary(reference_element, sample_element):
    keys_to_pop = []
    for key, value in sample_element.items():
        if key in reference_element:
            if isinstance(value, dict):
                clean_dictionary(reference_element[key], value)
        else:
            keys_to_pop.append(key)

    for key in keys_to_pop:
        print("Removing element:", key)
        sample_element.pop(key)


def compare_overlay_to_default(file_name, overlay_settings):
    print("Comparing settings file:", file_name)
    default_config_folder = "/usr/local/default_configuration/"
    ffp = os.path.join(default_config_folder, file_name)
    if os.path.exists(ffp) is False:
        print("Default file not found", file_name, "may no longer exist!!!")
        return overlay_settings

    with open(ffp, "r") as jfi:
        default_settings = json.load(jfi)

    clean_dictionary(default_settings, overlay_settings)

    return overlay_settings


def read_files_in_overlay(path):
    for root, folders, files in os.walk(path):
        for file in files:
            if file[-4:] != "json":
                print("skipping file", file)
                continue

            ffp = os.path.join(root, file)
            with open(ffp, "r") as jfi:
                settings = json.load(jfi)

            modified_settings = compare_overlay_to_default(file, settings)
            modified_settings = remove_empty_elements(modified_settings)

            with open(ffp, "w") as jfo:
                json.dump(modified_settings, jfo, indent=4, sort_keys=True)


def get_overlay_path():
    home = str(os.path.expanduser("~"))
    ffp = os.path.join(home, ".instrument", "launch.json")
    with open(ffp, "r") as sfi:
        launch = json.load(sfi)

    return os.path.expanduser(launch["paths"]["overlay_configuration"])

def check_if_in_config(filename):
    default_file_path = os.path.join("/usr/local/default_configuration", filename)
    return os.path.exists(default_file_path)


def remove_unexpected_overlays(overlay_dir):
    expected_overlays = [
        "console_client.json",
        "NamedLocation.json",
        "plate_handler.json",
        "PlateHandlerNamedLocation.json"
    ]
    try:
        os.remove(os.path.join(overlay_dir, "UltrasonicSubsystemConfig.json"))
        print("Removing UltrasonicSubsystemConfig.json which is no longer an expected overlay in 5.6.6")
    except:
        print("File UltrasonicSubsystemConfig.json wasn't present in the directory")
        
    for root, folders, files in os.walk(overlay_dir):
        for file in files:
            if file[-4:] != "json":
                print("skipping file %r which is not a configuration file" % file)
                continue

            if file in expected_overlays:
                print("skipping file %r which is expected" % file)
                continue

            in_config = check_if_in_config(file)

            if not in_config:
                print("skipping %r which is not in the default configuration folder" % file)
                print("note, %r may be a formerly valid configuration file but it no longer used" % file)
                continue

            print("removing %r which is no longer an expected overlay in 5.6.6" % file)
            os.remove(os.path.join(root, file))
        

if __name__ == '__main__':
    overlay_path = get_overlay_path()
    backup_overlays()
    print("Cleaning up overlays in", overlay_path)
    read_files_in_overlay(overlay_path)
    print("Removing unexpected overlays in", overlay_path)
    remove_unexpected_overlays(overlay_path)
    update_sw_icsgui_fw()
    print("THANKS FOR UPDATING, SEE YOU SOON!")
    
