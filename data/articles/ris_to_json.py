import json
import re
import os
import argparse
import sys

def parse_ris(file_path):
    ris_mapping = {
        "PMID": "pmid",
        "T1": "title",
        "TI": "title",
        "FAU": "authors",
        "TA": "jrnl",
        "JT": "journal",
        "PY": "year",
        "DP": "year",
        "VI": "volume",
        "IP": "number",
        "PG": "pages",
        "LID": "doi",
        "AID": "doi",
        "OT": "keywords",
        "FT": "featured",
        "SP": "start_page",
        "EP": "end_page",
    }
    
    data = {}
    authors = []
    keywords = []
    dois = []
    use_fau = False
    current_key = None
    start_page = None
    end_page = None
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.match(r"^(\w{2,4})\s*-\s*(.*)$", line)
            if match:
                key, value = match.groups()
                key = key.strip()
                value = value.strip()
                current_key = key
                
                if key == "FAU":
                    use_fau = True
                    authors.append(parse_author(value))
                elif key == "AU" and not use_fau:
                    authors.append(parse_author(value))
                elif key in ris_mapping:
                    json_key = ris_mapping[key]
                    
                    if json_key == "keywords":
                        keywords.append(value)
                    elif json_key == "doi":
                        if "10." in value:
                            dois.append(value)
                    elif json_key == "year":
                        data[json_key] = value.split()[0]  # Extracting just the year
                    elif json_key == "start_page":
                        start_page = value
                    elif json_key == "end_page":
                        end_page = value
                    else:
                        data[json_key] = value
            elif current_key == "TI":  # Handle multiline title
                data["title"] += " " + line.strip()
    
    if authors:
        data["authors"] = authors
    if keywords:
        data["keywords"] = keywords
    if dois:
        data["url"] = f"https://doi.org/{dois[0]}"  # Use the first DOI found
    if "pages" not in data and start_page:
        if end_page:
            data["pages"] = f"{start_page}-{end_page}"
        else:
            data["pages"] = f"{start_page}"
    data["status"] = "published"
    
    return data


def format_names(name_list):
    formatted_names = []
    for entry in name_list:
        firstnames = entry['firstname'].split()
        initials = ''.join([name[0] for name in firstnames])  # Extract initials
        formatted_names.append(f"{entry['surname']} {initials}")
    return formatted_names
    
    
def print_as_text(articles, max_authors: int):
    format_str = "{}\n{}\n{} {}, {}({}), {}\n{}"
    for a in articles:
        if len(a["authors"]) > max_authors:
            authors = ", ".join(format_names(a["authors"][:4])) + " et al."
        else:
            authors = ", ".join(format_names(a["authors"]))
        issue = a.get("number","")
        print(format_str.format(a["title"], 
    			authors,
    			a["jrnl"], a["year"], a["volume"], issue, a["pages"],
    			a["url"]));


def parse_author(name):
    parts = name.split(", ")
    if len(parts) == 2:
        return {"firstname": parts[1], "surname": parts[0]}
    return {"firstname": "", "surname": name}
    
    
def process_folder(folder_path):
    entries = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".ris"):
                file_path = os.path.join(root, file)
                try:
                    entries.append(parse_ris(file_path))
                except:
                    print("Can't parse:",file_path,file=sys.stderr)
    return entries
    

def main():
    parser = argparse.ArgumentParser(description="Convert an RIS file to JSON format.")
    parser.add_argument("-i", "--input" , help="Path to the input RIS file")
    parser.add_argument("-p", "--print" , help="Print all citations as text", action='store_true')
    parser.add_argument("-o", "--output", help="Path to the output JSON file. If not specified, prints to screen.")
    parser.add_argument("-f", "--folder", help="Path to a folder containing RIS files to process recursively.")
    parser.add_argument("--full", help="Print the full entry, include all authors", action='store_true')
    
    args = parser.parse_args()
    
    if args.folder:
        citation_data = process_folder(args.folder)
    elif args.input:
        citation_data = [parse_ris(args.input)]
    else:
        print("Error: Either -i (input file) or -f (folder) must be specified.")
        return
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as json_file:
            json.dump(citation_data, json_file, indent=4, ensure_ascii=False)
        print(f"Converted {args.input} to {args.output}")
    elif args.print:
        max_authors = 100 if args.full else 5
        print_as_text(citation_data, max_authors)
    else:
        print(json.dumps(citation_data, indent=4, separators=(",", ":"), ensure_ascii=False))

if __name__ == "__main__":
    main()

