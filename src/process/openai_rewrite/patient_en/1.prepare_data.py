import jsonlines
import json
import argparse

query_prompt = """
<text>{text}</text>
Please create some dialogues between patients and doctors in English based on the above text. The format is:
<Patient>Patient’s question</Patient>
<Doctor>Doctor’s answer</Doctor>
Both patient questions and doctor responses are as complex and detailed as possible."""


def generate_query(data):
    chatgpt_query = query_prompt.format_map({"text": data[0]})
    return chatgpt_query


def Prepare_data(args):
    data = []
    # Read the uploaded JSONl file
    with jsonlines.open(args.input_path, "r") as reader:
        data = list(reader)

    print(f"len:{len(data)}")
    # Convert as required
    jsonl_data = []

    for id, item in enumerate(data):
        query = generate_query(item)
        if len(query) > 4090:
            continue
        jsonl_data.append(
            {
                "id": id,
                "query": generate_query(item),
                "model_answer": "",
                "reference": item[0],
            }
        )

    # Save the converted data as a JSONL file
    with open(args.output_path, "w", encoding="utf-8") as file:
        for entry in jsonl_data:
            file.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Prepare finished, output to '{args.output_path}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare data for OpenAIGPT generation"
    )
    parser.add_argument(
        "--input_path", type=str, required=True, help="Path to the input JSON file."
    )
    parser.add_argument(
        "--output_path", type=str, required=True, help="Path to the output JSONL file."
    )
    args = parser.parse_args()
    Prepare_data(args)
