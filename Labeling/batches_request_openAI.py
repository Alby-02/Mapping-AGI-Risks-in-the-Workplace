from openai import OpenAI
import json, time
client = OpenAI()

UPLOAD_FUNCTION = False

input_file = "batch_input_full_no_patents.jsonl"
output_file = "output_full_no_patents.jsonl"

if not UPLOAD_FUNCTION:
    print("Using existing batch ID. Skipping upload.")
    batch_id = "batch_6a01df7aaf1c8190be0301c221dab5df" # Replace with your actual batch ID if RETRIEVE_EXISTING_BATCH is True

# Upload
if UPLOAD_FUNCTION:
    #confirm option to upload or not
    confirm = input("Do you want to upload a new batch input file? (y/n): ")
    if confirm.lower() != 'y':
        print("Upload cancelled. Exiting.")
        exit(0)
    print("Uploading batch input file...")

    f = client.files.create(file=open(input_file, "rb"), purpose="batch")

    # Create batch
    batch = client.batches.create(
        input_file_id=f.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    print(f"Batch created: {batch.id} | Status: {batch.status}")
    with open("outputBatchIDs.txt", "a", encoding="utf-8") as f:
        f.write(f"\nBatch ID: {batch.id}")


# Wait for batch to complete

max_wait_time = 300
wait_interval = 15    # Check every 15 seconds
elapsed_time = 0

if not UPLOAD_FUNCTION:
    batch = client.batches.retrieve(batch_id)
else:
    batch = client.batches.retrieve(batch.id)

while batch.status not in ['completed', 'failed', 'cancelled']:
    if elapsed_time >= max_wait_time:
        print(f"Timeout: Batch did not complete within {max_wait_time} seconds")
        break

    print(f"Batch status: {batch.status}. Waiting {wait_interval} seconds...")
    time.sleep(wait_interval)
    elapsed_time += wait_interval
    # Refresh batch status
    batch = client.batches.retrieve(batch.id)

print(f"Final batch status: {batch.status}")

# save results
if batch.status == 'completed' and batch.output_file_id:
    print("Downloading results...")
    result = client.files.content(batch.output_file_id)
    with open(output_file, "a", encoding="utf-8") as f:
        for line in result.text.strip().split("\n"):
            obj = json.loads(line)
            cid = obj["custom_id"]
            text = obj["response"]["body"]["choices"][0]["message"]["content"]
            f.write(f"\n[{cid}]\n{text}\n")
    print("Results saved to outputTest.jsonl")
elif batch.status == 'failed':
    print("Batch failed. Checking for error details...")
    if batch.error_file_id:
        error_result = client.files.content(batch.error_file_id)
        print("Error details:")
        print(error_result.text)
    else:
        print("No error details available.")
elif batch.status == 'cancelled':
    print("Batch was cancelled.")
else:
    print(f"Batch is still in status: {batch.status}. Please check back later.")
