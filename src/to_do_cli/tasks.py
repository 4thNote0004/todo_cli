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
