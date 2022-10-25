from dsqueue.double_stack_queue import DoubleStackQueue

if __name__ == '__main__':
    queue = DoubleStackQueue(max_size=3)

    items = [f"item_{i}" for i in range(20)]
    idx = 0
    for i in range(20):
        print(f"\t--- Step {i} ---")
        if not queue.full():
            print(f"+ Put {items[idx]} into queue")
            queue.put(items[idx])
            idx += 1
        else:
            data = queue.pop()
            print(f"- Pop {data} out of queue")

    # Pop out any item still remain in queue:
    while not queue.empty():
        data = queue.pop()
        print(f"- Pop out: {data}")
