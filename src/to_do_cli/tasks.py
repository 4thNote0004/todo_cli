from to_do_cli.storage import load_tasks, save_tasks


def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"✔ Task added: {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("no tasks yet!")
        return

    for i, t in enumerate(tasks, 1):
        status = "✓" if t["done"] else "✗"
        print(f"{i}. [{status}] {t['title']}")


def update_task(index, new_title=None, done=None):
    tasks = load_tasks()

    if index < 0 or index >= len(tasks):
        print("❌ invalid index")
        return

    task = tasks[index]

    if new_title is not None:
        task["title"] = new_title

    if done is not None:
        task["done"] = done

    save_tasks(tasks)
    print(f"✔ Task updated: {task['title']}")


def delete_task(index):
    tasks = load_tasks()

    if index < 0 or index >= len(tasks):
        print("❌ Invalid index.")
        return

    removed = tasks.pop(index)
    save_tasks(tasks)

    print(f"✔ Task deleted: {removed['title']}")
