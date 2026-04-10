import tkinter as tk
from tkinter import messagebox

BG = "#0f172a"
CARD = "#1e293b"
TEXT = "#e2e8f0"
ACCENT = "#38bdf8"

# ---------- Algorithms ----------
def fcfs(processes):
    time = 0
    result = []
    gantt = []

    for p in processes:
        if time < p[1]:
            time = p[1]

        wt = time - p[1]
        time += p[2]
        tat = wt + p[2]

        result.append((p[0], wt, tat))
        gantt.append((p[0], p[2]))

    return result, gantt

def sjf(processes):
    processes = sorted(processes, key=lambda x: x[2])
    return fcfs(processes)

def round_robin(processes, quantum):
    time = 0
    rem = [p[2] for p in processes]
    result = [None]*len(processes)
    gantt = []

    while any(r > 0 for r in rem):
        for i, p in enumerate(processes):
            if rem[i] > 0:
                exec_time = min(quantum, rem[i])
                gantt.append((p[0], exec_time))
                time += exec_time
                rem[i] -= exec_time

                if rem[i] == 0:
                    wt = time - p[2] - p[1]
                    tat = wt + p[2]
                    result[i] = (p[0], wt, tat)

    return result, gantt

# ---------- UI Functions ----------
def get_processes():
    processes = []
    for i in range(len(entries)):
        at = int(entries[i][0].get())
        bt = int(entries[i][1].get())
        processes.append((i+1, at, bt))
    return processes

def display(result, gantt):
    output.delete("1.0", tk.END)

    output.insert(tk.END, "PID\tWT\tTAT\n")
    output.insert(tk.END, "-"*25 + "\n")

    for r in result:
        output.insert(tk.END, f"P{r[0]}\t{r[1]}\t{r[2]}\n")

    # Draw Gantt Chart
    canvas.delete("all")
    x = 10
    for p, t in gantt:
        width = t * 30
        canvas.create_rectangle(x, 20, x+width, 60, fill=ACCENT)
        canvas.create_text(x+width/2, 40, text=f"P{p}", fill="black")
        x += width

def run_fcfs():
    try:
        res, gantt = fcfs(get_processes())
        display(res, gantt)
    except:
        messagebox.showerror("Error", "Invalid Input")

def run_sjf():
    try:
        res, gantt = sjf(get_processes())
        display(res, gantt)
    except:
        messagebox.showerror("Error", "Invalid Input")

def run_rr():
    try:
        q = int(q_entry.get())
        res, gantt = round_robin(get_processes(), q)
        display(res, gantt)
    except:
        messagebox.showerror("Error", "Invalid Input")

def generate():
    global entries
    entries = []

    for widget in frame_inputs.winfo_children():
        widget.destroy()

    n = int(n_entry.get())

    for i in range(n):
        tk.Label(frame_inputs, text=f"P{i+1}", bg=CARD, fg=TEXT).grid(row=i, column=0)

        at = tk.Entry(frame_inputs, width=5)
        at.grid(row=i, column=1)

        bt = tk.Entry(frame_inputs, width=5)
        bt.grid(row=i, column=2)

        entries.append((at, bt))

# ---------- UI ----------
root = tk.Tk()
root.title("CPU Scheduler Pro")
root.geometry("700x650")
root.configure(bg=BG)

tk.Label(root, text="CPU Scheduling Simulator", font=("Arial", 16, "bold"),
         bg=BG, fg=ACCENT).pack(pady=10)

card = tk.Frame(root, bg=CARD, padx=10, pady=10)
card.pack(pady=10)

tk.Label(card, text="Number of Processes", bg=CARD, fg=TEXT).pack()
n_entry = tk.Entry(card)
n_entry.pack()

tk.Button(card, text="Generate Inputs", command=generate, bg=ACCENT).pack(pady=5)

frame_inputs = tk.Frame(card, bg=CARD)
frame_inputs.pack()

tk.Label(card, text="Time Quantum", bg=CARD, fg=TEXT).pack()
q_entry = tk.Entry(card)
q_entry.pack()

btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="FCFS", command=run_fcfs, bg=ACCENT, width=10).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="SJF", command=run_sjf, bg=ACCENT, width=10).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Round Robin", command=run_rr, bg=ACCENT, width=12).grid(row=0, column=2, padx=5)

output = tk.Text(root, height=8, bg="#020617", fg=TEXT)
output.pack(pady=10)

canvas = tk.Canvas(root, height=100, bg=BG, highlightthickness=0)
canvas.pack()

root.mainloop()