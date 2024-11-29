def ask(prompt, token, temp, model, streamprint=True, linktoanotherserver=False, mode="text"):
    # Set API key
    if model[:3] == "gpt":
        os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
        api_key = os.getenv("OPENAI_API_KEY")
    else:
        os.environ["OPENAI_API_KEY"] = "EMPTY"
        api_key = os.getenv("OPENAI_API_KEY")

    # Set API base URL
    if model[:3] == "gpt":
        api_base = 'https://api.openai.com/v1'
    elif '/' in model or 'local' in model:
        if os.path.isdir("/path/to/your/local/directory"):
            api_base = "http://localhost:8000/v1"
        else:
            api_base = "http://localhost:8001/v1"
    else:
        api_base = "http://localhost:11434/v1"

    # Check if connection to another server is needed
    if linktoanotherserver and ('/' in model or 'local'):
        api_base = "http://localhost:8001/v1"
    
    if model == "gpto1":
        setmodel = 'o1-preview'
    elif model == "gpto1mini":
        setmodel = "o1-mini"
    elif model == "gpt4":
        setmodel = 'gpt-4o'
    elif model == "gpt4mini":
        setmodel = "gpt-4o-mini"
    elif model == "gpt4t":
        setmodel = "gpt-4-turbo"
    elif model == "local":
        client = OpenAI(api_key=api_key, base_url=api_base)
        setmodel = re.search(r"id='(.*?)', created=", str(client.models.list())).group(1) if re.search(r"id='(.*?)', created=", str(client.models.list())) else None
    else:
        client = OpenAI(api_key=api_key, base_url=api_base)
    
    if streamprint:
        print('Stream print report model is:', setmodel)

    # Process requests in different modes
    if mode == "image":
        # For image mode, use pre-constructed messages with corresponding temperature and token values
        chat_completion_from_base64 = client.chat.completions.create(
            messages=prompt,
            model=setmodel,
            max_tokens=token,
            temperature=temp,
        )
        final_response = chat_completion_from_base64.choices[0].message.content
        print(f"Chat completion output (image mode): {final_response}")
    
    # Text mode processing
    else:
        if "o1" not in setmodel:
            stream = client.chat.completions.create(
                model=setmodel,
                messages=prompt,
                stream=True,
                max_tokens=token,
                temperature=temp,
            )
            final_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    if streamprint:
                        print(chunk.choices[0].delta.content, end="")
                    final_response += chunk.choices[0].delta.content
        else:
            final_response = client.chat.completions.create(
                model=setmodel,
                messages=prompt,
            )
            final_response = final_response.choices[0].message.content

    # Save record to a dictionary
    record = {
        "prompt": prompt,
        "setmodel": setmodel,
        "temp": temp,
        "max_tokens": token,
        "response": final_response
    }

    # Generate folder and file name
    now = datetime.now()
    date_str = now.strftime("%y%m%d")
    
    # Process prompt, remove non-alphanumeric characters, and truncate to first 30 characters
    prompt_str = re.sub(r'\W+', '', str(prompt))[:30]
    
    folder_path = f"/path/to/your/history/directory/{setmodel}/{date_str}"
    os.makedirs(folder_path, exist_ok=True)

    # Check for unique file name
    max_digits = 100
    current_digits = 3

    while current_digits <= max_digits:
        random_suffix = f"{random.randint(10**(current_digits-1), 10**current_digits - 1)}"
        file_name = f"{prompt_str}RANDOMKEY{random_suffix}.pkl"
        file_path = os.path.join(folder_path, file_name)
        
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                pickle.dump(record, f)
            break
        
        current_digits += 1

    if current_digits > max_digits:
        raise RuntimeError("Unable to generate a unique file name after exhausting all possible options.")

    return final_response

def upload_RUN_PAY_jsonl(jsonl_input, description='default description', do_it_now=False, jobtype="chat"):
    # Uploads a JSONL file to OpenAI and returns the file ID and batch request ID
    
    # Check input type and handle file path
    if isinstance(jsonl_input, str):
        jsonl_file = open(jsonl_input, 'rb')
        jsonl_filepath = jsonl_input
    elif isinstance(jsonl_input, io.StringIO):
        jsonl_file = io.BytesIO(jsonl_input.getvalue().encode('utf-8'))
        jsonl_filepath = "in_memory_file.jsonl"
    else:
        jsonl_file = jsonl_input
        jsonl_filepath = getattr(jsonl_input, 'name', "in_memory_file.jsonl")
    
    if do_it_now == "Fake":
        display(HTML(f"<span style='color: red;'>Warning: This is a simulated operation and will not actually execute.</span>"))
        return None 
    
    # Confirm execution
    if not do_it_now:
        confirmation = input("Enter y/Y/1 to confirm running this function: ")
        if confirmation not in ('y', 'Y', '1'):
            print("Operation canceled.")
            return None

    try:
        # Upload to OpenAI API
        os.environ["OPENAI_API_KEY"] = "%USER_API_KEY%"
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = 'https://api.openai.com/v1'
        client = OpenAI(api_key=api_key, base_url=api_base)
        
        # Upload file
        uploaded_file = client.files.create(
            file=jsonl_file,
            purpose="batch"
        )
        
        # If the first line contains 'embeddings', set the endpoint to '/v1/embeddings'
        if jobtype == "embedding":
            print("Detected 'embeddings' in the first line, setting endpoint to '/v1/embeddings'")
            endpoint = "/v1/embeddings"
        else:
            endpoint = "/v1/chat/completions"
        
        # Create batch
        batch_status = client.batches.create(
            input_file_id=uploaded_file.id,
            endpoint=endpoint,
            completion_window="24h",
            metadata={
                "description": description
            }
        )
        print("Batch request sequence ID (batch_id) returned:", batch_status.id)
        return {"batch_id": batch_status.id}
    finally:
        jsonl_file.close()
      
        
def auto_down_ans(id, max_wait_time=60, jobtype="chat", forceid=''):
    """
    Attempts to download a JSONL file, querying every 3 seconds initially, then every 1 minute after 10 minutes,
    until the maximum wait time is reached.

    Parameters:
    - id: Identifier of the file
    - max_wait_time: Maximum wait time (in minutes), default is 60 minutes
    - jobtype: Task type, default is "chat"
    - forceid: Forced file ID, default is an empty string

    Returns:
    - Downloaded content on success
    - None if maximum wait time is reached
    """
    max_wait_time_seconds = max_wait_time * 60
    start_time = time.time()
    file_id = forceid if len(forceid) > 0 else id
    mode = "Using forceid" if len(forceid) > 0 else "Using variable id"
    mode_color = 'blue' if len(forceid) > 0 else 'green'

    while True:
        clear_output(wait=True)
        current_time = datetime.now().strftime("%H:%M:%S")
        elapsed_time = time.time() - start_time
        elapsed_str = str(timedelta(seconds=int(elapsed_time)))

        display(HTML(f"<p>Current mode: <b style='color:{mode_color};'>{mode}</b>, File ID: <b style='color:orange;'>{file_id}</b></p>"))
        display(HTML(f"<p>Current time: <b>{current_time}</b></p>"))
        display(HTML(f"<p>Elapsed time: <b>{elapsed_str}</b></p>"))
        display(HTML('<p style="color:red;">Processing...</p>'))

        if jobtype == "chat":
            try:
                download = download_jsonl(file_id)
                ans = download['answer']
                if ans is not None:
                    clear_output(wait=True)
                    total_time_str = str(timedelta(seconds=int(time.time() - start_time)))
                    display(HTML(f"<p>Current mode: <b style='color:{mode_color};'>{mode}</b>, File ID: <b style='color:orange;'>{file_id}</b></p>"))
                    display(HTML(f"<p>Current time: <b>{current_time}</b></p>"))
                    display(HTML(f"<p>Total time: <b>{total_time_str}</b></p>"))
                    display(HTML('<p style="color:green;">Completed!</p>'))

                    fullstatus = download['fullstatus']
                    completed = fullstatus.request_counts.completed
                    total = fullstatus.request_counts.total
                    failed = fullstatus.request_counts.failed

                    html_content = f"""
                    <p>
                        Completed: <b style='color:green'>{completed}</b> &nbsp;&nbsp;
                        Total: <b style='color:blue'>{total}</b> &nbsp;&nbsp;
                        Failed: <b style='color:red'>{failed}</b>
                    </p>
                    """
                    display(HTML(html_content))

                    if fullstatus.request_counts.failed > 0:
                        print("Failed request IDs:", download['errorid'])
                        errordf = download['errordf']
                        errordf.rename(columns={'response.body.error.message': 'ans'}, inplace=True)
                        
                        correctdf = download['responsedf']
                        correctdf['ans'] = [correctdf.loc[x, 'response.body.choices'][0]['message']['content'] for x in range(len(correctdf))]
                        merged_df = pd.concat([errordf, correctdf], ignore_index=True)
                        merged_df["custom_id"] = merged_df["custom_id"].astype(int)
                        merged_df = merged_df.sort_values(by="custom_id").reset_index(drop=True)

                        if fullstatus.request_counts.total == len(merged_df["ans"].tolist()):
                            display(HTML('<p style="color:yellow;">Answer count matches total requests, but errors exist.</p>'))
                            return merged_df["ans"].tolist()
                        else:
                            display(HTML('<p style="color:red;">Answer count does not match total requests, sleeping for 600 seconds.</p>'))
                            time.sleep(600)

                    if fullstatus.request_counts.total == len(ans):
                        display(HTML('<p style="color:green;">Answer count matches total requests.</p>'))
                        return ans
                    else:
                        display(HTML('<p style="color:red;">Answer count does not match total requests, sleeping for 600 seconds.</p>'))
                        time.sleep(600)
                else:
                    fullstatus = download['fullstatus']
                    completed = fullstatus.request_counts.completed
                    total = fullstatus.request_counts.total
                    failed = fullstatus.request_counts.failed
                    html_content = f"""
                    <p>
                        Completed: <b style='color:green'>{completed}</b> &nbsp;&nbsp;
                        Total: <b style='color:blue'>{total}</b> &nbsp;&nbsp;
                        Failed: <b style='color:red'>{failed}</b>
                    </p>
                    """
                    display(HTML(html_content))
            except Exception as e:
                print(f'Download failed, error: {e}')
                
        if jobtype == "embedding":
            try:
                os.environ["OPENAI_API_KEY"] = "%USER_API_KEY%"
                api_key = os.getenv("OPENAI_API_KEY")
                api_base = 'https://api.openai.com/v1'
                client = OpenAI(api_key=api_key, base_url=api_base)
                full_status = client.batches.retrieve(file_id)
                outputid = full_status.output_file_id
                file_response = client.files.content(outputid)
                ans_text = file_response.text
                list_embedding = [json.loads(line)['response']['body']['data'][0]['embedding'] 
                                  for line in ans_text.split("\n") if line.strip()]
                
                clear_output(wait=True)
                total_time_str = str(timedelta(seconds=int(time.time() - start_time)))
                display(HTML(f"<p>Current mode: <b style='color:{mode_color};'>{mode}</b>, File ID: <b style='color:orange;'>{file_id}</b></p>"))
                display(HTML(f"<p>Current time: <b>{current_time}</b></p>"))
                display(HTML(f"<p>Total time: <b>{total_time_str}</b></p>"))
                display(HTML('<p style="color:green;">Completed!</p>'))
                    
                return list_embedding
            
            except Exception as e:
                print(f'Embedding process failed, error: {e}')
                
        if elapsed_time > max_wait_time_seconds:
            clear_output(wait=True)
            total_time_str = str(timedelta(seconds=int(elapsed_time)))
            display(HTML(f"<p>Current mode: <b style='color:{mode_color};'>{mode}</b>, File ID: <b style='color:orange;'>{file_id}</b></p>"))
            display(HTML(f"<p>Current time: <b>{current_time}</b></p>"))
            display(HTML(f"<p>Total time: <b>{total_time_str}</b></p>"))
            display(HTML('<p style="color:red;">Exceeded maximum wait time, download failed.</p>'))
            return None

        wait_time = 3 if elapsed_time < 600 else 60
        time.sleep(wait_time)

def download_jsonl(batchid, printstatus=True):
    """
    Download the results of a JSONL file using its batch ID and store the results in the 'answer' key as a list.

    Parameters:
    - batchid: The batch ID of the file.
    - printstatus: Whether to print the batch status. Default is True.

    Returns:
    - A dictionary containing batch status, answers, and additional data frames for successful and failed requests.
    """
    import os
    os.environ["OPENAI_API_KEY"] = "%USER_API_KEY%"
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = 'https://api.openai.com/v1'
    client = OpenAI(api_key=api_key, base_url=api_base)

    # Retrieve batch status
    full_status = client.batches.retrieve(batchid)
    status = full_status.status
    failed_count = full_status.request_counts.failed

    if failed_count > 0:
        print(f"{failed_count} requests failed.")
        print("Full status:", full_status)

    # Initialize result dictionary
    result = {
        "status": status,
        "answer": None,
        "fullstatus": full_status,
        "responsedf": None,
        "fullresponse": None,
        "errordf": None,
        "errorid": None
    }

    # Print batch status
    if printstatus:
        print(f"Batch status: {status}")

    def jsonl_to_dataframe(jsonl_data):
        import pandas as pd
        json_objects = []
        for line in jsonl_data.split('\n'):
            if line.strip():  # Skip empty lines
                try:
                    json_objects.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e} for line: {line}")
        return pd.json_normalize(json_objects)

    if failed_count > 0:
        print(f"Since {failed_count} requests failed, generating 'errordf' and 'errorid'.")
        
        # Get error file ID and fetch its content
        errorid = full_status.error_file_id
        file_error = client.files.content(errorid)
        
        # Print error file content
        print("Error details:", file_error.text)
        
        # Parse error file content and extract custom_id list
        errordf = jsonl_to_dataframe(file_error.text)
        result['errorid'] = errordf['custom_id'].astype(int).tolist()
        
        # Add error data to result dictionary
        result["errordf"] = errordf

    # If status is 'completed', fetch the file content
    if status == 'completed':
        outputid = full_status.output_file_id
        file_response = client.files.content(outputid)
        responsedf = jsonl_to_dataframe(file_response.text)
        
        # Convert custom_id to int, sort, and reset index
        responsedf['custom_id'] = responsedf['custom_id'].astype(int)
        responsedf.sort_values(by="custom_id", inplace=True)
        responsedf.reset_index(drop=True, inplace=True)
        
        # Extract responses
        responses = [responsedf.loc[x, 'response.body.choices'][0]['message']['content'] for x in range(len(responsedf))]
        result["answer"] = responses
        result["responsedf"] = responsedf
        result["fullresponse"] = file_response.text
        print("File content retrieved successfully. Check the 'answer' key in the result dictionary.")
    else:
        if printstatus:
            print("Batch status is not 'completed', skipping file content retrieval.")

    return result
