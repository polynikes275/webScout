#!/usr/bin/python3

import argparse
import subprocess
import os

def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="A tool to use FFUF, WFuzz, ds_walk, and iss_shortname with user-supplied flags and input files.")
    
    # Add arguments
    parser.add_argument("-f", "--file", required=False, help="Input file containing wordlists or directory paths")
    parser.add_argument("-m", "--mode", choices=["ffuf", "wfuzz", "ds-walk", "iis-shortname"], required=True, help="Choose the tool to run: 'ffuf', 'wfuzz', 'ds-walk (.ds_store enumeration)', 'iis-shortname scanner'")
    parser.add_argument("-u", "--url", required=True, help="Target URL to test")
    parser.add_argument("-w", "--wordlist", help="Specify a custom wordlist")
    parser.add_argument("--ffuf-flags", help="Additional flags to pass to ffuf")
    parser.add_argument("--wfuzz-flags", help="Additional flags to pass to wfuzz")

    # Parse arguments
    args = parser.parse_args()

    # Determine which tool to use based on the mode
    if args.mode == "ffuf":
        # Construct the ffuf command
        # Change as needed
        command = [
            "ffuf",
            "-w", args.wordlist if args.wordlist else args.file,
            "-u", f"{args.url}/FUZZ",
        ]
        
        if args.ffuf_flags:
            command.extend(args.ffuf_flags.split())

        print(f"Running FFUF: {' '.join(command)}")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"FFUF encountered an error: {e}")

    elif args.mode == "wfuzz":
        # Construct the wfuzz command
        # Change as needed
        command = [
            "wfuzz",
            "-w", args.wordlist if args.wordlist else args.file,
            "--hc", "404",
            args.url
        ]
        
        if args.wfuzz_flags:
            command.extend(args.wfuzz_flags.split())

        print(f"Running Wfuzz: {' '.join(command)}")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Wfuzz encountered an error: {e}")

    elif args.mode == "ds-walk":
        # Construct the ds-walk command
        # Change as needed
        dsWalkPath = os.path.abspath("ds_walk.py")
        if not os.path.isfile(dsWalkPath):
            print(f"Error: ds_walk.py not found at {dsWalkPath}")
            return
        
        command = [
            "python3", dsWalkPath,
            "-u", args.url,
        ]

        # Remove any empty strings from the command list
        command = [item for item in command if item]

        print(f"Running: {' '.join(command)}")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ds_walk.py encountered an error: {e}")

    elif args.mode == "iis-shortname":
        # Construct the iis-shortname command
        # Change as needed
        fname = "iis_shortname_scan.py"
        shortname = os.path.abspath(fname)
        if not os.path.isfile(shortname):
            print(f"\nError: iis_shortname_scan.py not found at {shortname}\n")
            return

        command = [
            "python3", shortname,
            args.url
        ]
        

        print(f"\nRunning: {' '.join(command)}\n")
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"{shortname} encountered an error: {e}")



if __name__ == "__main__":
    main()

