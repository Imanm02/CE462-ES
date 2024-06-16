def rate_monotonic_scheduling(tasks):
    tasks = sorted(tasks, key=lambda x: x[1])
    schedule = []
    time = 0
    while True:
        if not any(task[2] > 0 for task in tasks):
            break
        for task in tasks:
            period = task[1]
            exec = task[2]
            if time % period == 0:
                task[3] = time + period
            if time >= task[3]:
                task[2] = exec
                task[3] += period
            if task[2] > 0:
                task[2] -= 1
                schedule.append(task[0])
                break
        time += 1
    return schedule


def get_tasks():
    n = int(input("Enter tasks count: "))
    tasks = []
    for i in range(n):
        name = input(f"task {i}'s name: ")
        period = int(input(f"task {i}'s period: "))
        execution_time = int(input(f"task {i}'s execution time: "))
        tasks.append([name, period, execution_time, period])
    return tasks


if __name__ == "__main__":
    tasks = get_tasks()
    schedule = rate_monotonic_scheduling(tasks)
    print("Schedule:", schedule)