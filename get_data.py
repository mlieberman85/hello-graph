from copy import deepcopy
import json
import os
import subprocess
import sys


def process(d: dict, to_file: bool=True):
    for k,v in d.items():
        x = deepcopy(v)
        d = process_drv(x)
        drv_to_output_dict = drv_to_output(k, v)
        if to_file:
            file = f"{os.path.basename(os.path.normpath(k))}.json"
            path = os.path.join("drvmod/", file)

            with open(path, 'w') as f:
                    json.dump(x, f)

            file = f"{os.path.basename(os.path.normpath(k))}.output.json"
            path = os.path.join("drvmod/", file)

            with open(path, 'w') as f:
                    json.dump(drv_to_output_dict, f)



    return d

def drv_to_output(drv_path: str, drv: dict):
    output_hash = get_nix_hash(drv_path)
    input = drv["outputs"]["out"]["path"]
    output_dict = {
        "outputs": {
            "name": drv_path,
            "digest": { "sha256": output_hash },
        },
        "args": [],
        "env": {},
        "builder": "http://nixos.org/drv/0.1",
        "inputs": [
            {
                "uri": f"file://{input}",
                "digest": {
                    "sha256": get_nix_hash(input)
                }
            }
        ],
    }

    return output_dict

def process_drv(v: dict):
    # Get Nix hash of output
    output = v["outputs"]["out"]["path"]
    output_hash = get_nix_hash(output)
    output_dict = {
        "name": output,
        "digest": { "sha256": output_hash }
    }

    v["outputs"] = output_dict

    # Get Nix hashes of input srcs
    input_srcs = v["inputSrcs"]
    input_srcs_list = [{
            "uri": f"file://{input_src}",
            "digest": {
                "sha256": get_nix_hash(input_src)
            }
        } for input_src in input_srcs
    ]

    v["inputs"] = input_srcs_list

    # Get Nix hashs of input drvs
    input_drvs = v["inputDrvs"]
    input_drvs_list = [{
            "uri": f"file://{input_drv}",
            "digest": {
                "sha256": get_nix_hash(input_drv)
            }
        } for input_drv, _ in input_drvs.items()
    ]

    v["inputs"] += input_drvs_list

    return v

def get_nix_hash(p: str):
    process = subprocess.Popen(["nix-hash", p, "--type", "sha256"],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE,
                     universal_newlines=True)
    stdout, _ = process.communicate()
    # If the store path doesn't exist locally, check nix-cache
    if (hash := stdout.strip()) == "":
        hash = get_nix_hash_from_narinfo(p)

    return hash

def get_nix_hash_from_narinfo(p: str):
    process = subprocess.Popen(["./get_hash_from_narinfo.sh", p],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)
    stdout, _ = process.communicate()

    return stdout.strip()


if __name__ == "__main__":
    with open(sys.argv[1]) as j:
        d = process(json.load(j))
        #print(json.dumps(d))
