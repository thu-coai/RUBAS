import json
import os 

def sort_count_dict(counts):
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def markdown_table(title, counts):
    lines = [f"## {title}", "", "| Name | Count |", "| --- | ---: |"]
    for name, count in counts.items():
        lines.append(f"| {name} | {count} |")
    lines.append("")
    return "\n".join(lines)


def _read_existing_descriptions(info_path):
    if not os.path.exists(info_path):
        return {}

    descriptions = {}
    with open(info_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.split("|")[1:-1]]
            if len(cells) != 6 or cells[0] in {"Name", "---"}:
                continue
            descriptions[cells[0]] = cells[5]
    return descriptions


def get_data_info(direc):
    with open(f"{direc}/benign.json", "r") as f:
        benign_data = json.load(f)
    with open(f"{direc}/harmful.json", "r") as f:
        harmful_data = json.load(f)
    with open(f"{direc}/sensitive.json", "r") as f:
        sensitive_data = json.load(f)
    data_type = {"Benign": 0, "Harmful": 0, "Sensitive": 0}
    environments_count = {}
    harmful_environments_count = {}
    sensitive_environments_count = {}
    benign_environments_count = {}
    sensitive_risk_pattern_subtype = {}
    harmful_risk_pattern_subtype = {}
    harmful_risk_category = {}
    sensitive_risk_category = {}
   
    for item in benign_data + harmful_data + sensitive_data:
        data_type[item["data_type"]] += 1
        if item["data_type"] == "Harmful":
            for environment in item["environments"]:
                if environment["name"] not in harmful_environments_count:
                    harmful_environments_count[environment["name"]] = 0
                harmful_environments_count[environment["name"]] += 1
            if item["risk_pattern_subtype"] not in harmful_risk_pattern_subtype:
                harmful_risk_pattern_subtype[item["risk_pattern_subtype"]] = 0
            harmful_risk_pattern_subtype[item["risk_pattern_subtype"]] += 1
            if item["risk_category"] not in harmful_risk_category:
                harmful_risk_category[item["risk_category"]] = 0
            harmful_risk_category[item["risk_category"]] += 1
        if item["data_type"] == "Sensitive":
            for environment in item["environments"]:
                if environment["name"] not in sensitive_environments_count:
                    sensitive_environments_count[environment["name"]] = 0
                sensitive_environments_count[environment["name"]] += 1
            if item["risk_pattern_subtype"] not in sensitive_risk_pattern_subtype:
                sensitive_risk_pattern_subtype[item["risk_pattern_subtype"]] = 0
            sensitive_risk_pattern_subtype[item["risk_pattern_subtype"]] += 1
            if item["risk_category"] not in sensitive_risk_category:
                sensitive_risk_category[item["risk_category"]] = 0
            sensitive_risk_category[item["risk_category"]] += 1
        if item["data_type"] == "Benign":
            for environment in item["environments"]:
                if environment["name"] not in benign_environments_count:
                    benign_environments_count[environment["name"]] = 0
                benign_environments_count[environment["name"]] += 1
        for environment in item["environments"]:
            if environment["name"] not in environments_count:
                environments_count[environment["name"]] = 0
            environments_count[environment["name"]] += 1
    data_type = sort_count_dict(data_type)
    environments_count = sort_count_dict(environments_count)
    harmful_environments_count = sort_count_dict(harmful_environments_count)
    sensitive_environments_count = sort_count_dict(sensitive_environments_count)
    benign_environments_count = sort_count_dict(benign_environments_count)
    harmful_risk_pattern_subtype = sort_count_dict(harmful_risk_pattern_subtype)
    sensitive_risk_pattern_subtype = sort_count_dict(sensitive_risk_pattern_subtype)
    harmful_risk_category = sort_count_dict(harmful_risk_category)
    sensitive_risk_category = sort_count_dict(sensitive_risk_category)

    report_sections = [
        "# Data Info Report",
        "",
        f"Directory: `{direc}`",
        "",
        markdown_table("Data Type Summary", data_type),
        markdown_table("All Environments", environments_count),
        markdown_table("Harmful Environments", harmful_environments_count),
        markdown_table("Sensitive Environments", sensitive_environments_count),
        markdown_table("Benign Environments", benign_environments_count),
        markdown_table("Harmful Risk Pattern Subtype", harmful_risk_pattern_subtype),
        markdown_table("Sensitive Risk Pattern Subtype", sensitive_risk_pattern_subtype),
        markdown_table("Harmful Risk Category", harmful_risk_category),
        markdown_table("Sensitive Risk Category", sensitive_risk_category),
    ]
    report = "\n".join(report_sections)
    output_path = f"{direc}/data_info.md"

    with open(output_path, "w") as f:
        f.write(report)

    print(f"Saved report to {output_path}")

def get_train_data_info(direc):
    output_path = f"{direc}/info.md"
    existing_descriptions = _read_existing_descriptions(output_path)
    rows = []

    for file in sorted(os.listdir(direc)):
        if not file.endswith(".json"):
            continue

        with open(f"{direc}/{file}", "r") as f:
            data = json.load(f)

        counts = {"Harmful": 0, "Sensitive": 0, "Benign": 0}
        for item in data:
            data_type = item.get("data_type")
            if data_type in counts:
                counts[data_type] += 1

        rows.append(
            {
                "name": file,
                "harmful": counts["Harmful"],
                "sensitive": counts["Sensitive"],
                "benign": counts["Benign"],
                "total": len(data),
                "description": existing_descriptions.get(file, ""),
            }
        )

    rows.sort(key=lambda row: row["name"])

    report_lines = [
        "# Train Data Info",
        "",
        f"Directory: `{direc}`",
        "",
        "| Name | Harmful | Sensitive | Benign | Total | Description |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]

    for row in rows:
        report_lines.append(
            f'| {row["name"]} | {row["harmful"]} | {row["sensitive"]} | {row["benign"]} | {row["total"]} | {row["description"]} |'
        )

    report_lines.append("")

    with open(output_path, "w") as f:
        f.write("\n".join(report_lines))

    print(f"Saved report to {output_path}")



def main():
    get_train_data_info("./data/trainset")

if __name__ == "__main__":
    main()
