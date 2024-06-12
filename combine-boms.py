import csv
from collections import defaultdict

def read_bom(file_path, pcb_name):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        bom = []
        for row in reader:
            designators = row["Designator"].split(',')
            prefixed_designators = [f"{pcb_name}-{d.strip()}" for d in designators]
            row["Designator"] = ','.join(prefixed_designators)
            bom.append(row)
        return bom

def combine_boms(bom_files):
    combined_bom = defaultdict(lambda: {"Designator": [], "Comment": None, "Footprint": None, "JLCPCB Part #": None})

    for pcb_name, file_path in bom_files.items():
        bom = read_bom(file_path, pcb_name)
        for item in bom:
            part_number = item["JLCPCB Part #"]
            combined_bom[part_number]["Designator"].extend(item["Designator"].split(','))
            combined_bom[part_number]["Comment"] = item["Comment"]
            combined_bom[part_number]["Footprint"] = item["Footprint"]
            combined_bom[part_number]["JLCPCB Part #"] = part_number

    # Format the combined BOM for output
    formatted_combined_bom = []
    for part_number, data in combined_bom.items():
        formatted_combined_bom.append({
            "Designator": ','.join(data["Designator"]),
            "Comment": data["Comment"],
            "Footprint": data["Footprint"],
            "JLCPCB Part #": part_number
        })

    return formatted_combined_bom

def write_combined_bom(combined_bom, output_file_path):
    fieldnames = ["Designator", "Comment", "Footprint", "JLCPCB Part #"]
    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in combined_bom:
            writer.writerow(row)

def main():
    bom_files = {
        "Board_0": "production-files/pcbs/tc2-main-pcb/tc2-main-pcb-bom.csv",
        "Board_1": "production-files/pcbs/tc2-plugs-buck-boost-pcb/tc2-plugs-buck-boost-pcb-bom.csv",
        
    }

    combined_bom = combine_boms(bom_files)
    output_file_path = "combined_bom.csv"
    write_combined_bom(combined_bom, output_file_path)
    print(f"Combined BOM saved to {output_file_path}")

if __name__ == "__main__":
    main()
