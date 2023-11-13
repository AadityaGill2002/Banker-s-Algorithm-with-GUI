import tkinter as tk
import numpy as np

def userInput():
    try:
        r, c = (int(i) for i in num_of_processes_resource.get().split())
        alloc = np.zeros((r, c))
        maximum = np.zeros((r, c))

        # Parse and populate the Allocation Matrix
        alloc_data = input_alloc.get("1.0", tk.END).strip().split("\n")
        for i in range(r):
            alloc[i] = np.array([int(val) for val in alloc_data[i].split()])

        # Parse and populate the Maximum Matrix
        max_data = input_max.get("1.0", tk.END).strip().split("\n")
        for i in range(r):
            maximum[i] = np.array([int(val) for val in max_data[i].split()])

        is_safe = input_safe.get().strip().lower()
        if is_safe == "yes":
            pass

        # Parse and populate the Available Resources
        avail_data = input_avail.get().strip().split()
        avail = np.array([int(val) for val in avail_data])

        is_request = input_request.get().strip().lower()
        if is_request == "yes":
            request_data = input_request_data.get().strip().split(";")
            requestID = int(request_data[0])
            requestVal = np.array([int(val) for val in request_data[1].split()])
        else:
            requestID, requestVal = -1, -1

    except:
        output_text.set("Incorrect values entered. Please try again.")
        return None

    return alloc, maximum, avail, requestID, requestVal

def safety(alloc, need, avail):
    n, m = alloc.shape
    work = avail.copy()
    finish = np.zeros(n)
    sequence = []

    while True:
        retry = 0
        for i in range(n):
            compare = need[i] <= work
            if finish[i] == 0 and compare.all():
                work = work + alloc[i]
                finish[i] = 1
                sequence.append(i)
                retry = 1
        if not retry:
            break

    for i in finish:
        if not i:
            return 0, []

    return 1, sequence

def request(alloc, need, avail, requestVal, requestID):
    if np.all(requestVal <= need[requestID]) and np.all(requestVal <= avail):
        alloc[requestID] += requestVal
        avail -= requestVal
        need[requestID] -= requestVal

        answer, _ = safety(alloc, need, avail)

        if answer:
            return 1
        else:
            # Roll back the allocation
            alloc[requestID] -= requestVal
            avail += requestVal
            need[requestID] += requestVal
    return -1

def update_text():
    alloc, maximum, avail, requestID, requestVal = userInput()

    if alloc is not None:
        need = maximum - alloc
        answer, sequence = safety(alloc, need, avail)

        need_label.config(text=f"Need matrix =\n{need}")

        if requestID > -1 and answer:
            result = request(alloc, need, avail, requestVal, requestID)
            if result == -1:
                result_label.config(text="Error, request cannot be granted. Unsafe state.")
            else:
                out = "Yes, request can be granted with a safe state, Safe state\n" if sequence else "Safe state\n"
                result_label.config(text=out)
                if sequence:
                    result_label.config(text=result_label.cget("text") + f"P{requestID}req, " + "".join(
                        [f"P{i}, " for i in sequence]).rstrip() + ".")
        else:
            out = "Yes, safe state" if answer else "No, unsafe state."
            result_label.config(text=out)
            if sequence:
                result_label.config(text=result_label.cget("text") + "<" + "".join(
                    [f"P{i}, " for i in sequence]).rstrip() + ">")

# Create a GUI window
root = tk.Tk()
root.title("Banker's Algorithm GUI")

# Create and layout widgets
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

instruction_label = tk.Label(frame, text="Enter data in the format: 'num_of_processes num_of_resource_types'")
instruction_label.pack()

num_of_processes_resource = tk.StringVar()
input_num = tk.Entry(frame, textvariable=num_of_processes_resource)
input_num.pack()

input_alloc_label = tk.Label(frame, text="Enter coefficients for the Allocation Matrix:")
input_alloc_label.pack()

input_alloc = tk.Text(frame, height=5, width=40)
input_alloc.pack()

input_max_label = tk.Label(frame, text="Enter coefficients for the Maximum Matrix:")
input_max_label.pack()

input_max = tk.Text(frame, height=5, width=40)
input_max.pack()

input_safe_label = tk.Label(frame, text="Ask about a safe state? (Yes/No):")
input_safe_label.pack()

input_safe = tk.Entry(frame)
input_safe.pack()

input_avail_label = tk.Label(frame, text="Enter the values of the available resources separated by space:")
input_avail_label.pack()

input_avail = tk.Entry(frame)
input_avail.pack()

input_request_label = tk.Label(frame, text="Add additional inquiries? (Yes/No):")
input_request_label.pack()

input_request = tk.Entry(frame)
input_request.pack()

input_request_data_label = tk.Label(frame, text="Enter process no. then ';' then the resource values separated by space:")
input_request_data_label.pack()

input_request_data = tk.Entry(frame)
input_request_data.pack()

submit_button = tk.Button(frame, text="Check Safety / Request", command=update_text)
submit_button.pack()

need_label = tk.Label(frame, text="")
need_label.pack()

result_label = tk.Label(frame, text="")
result_label.pack()

output_text = tk.StringVar()
output_label = tk.Label(frame, textvariable=output_text)
output_label.pack()

root.mainloop()
