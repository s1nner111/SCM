import sys
import zipfile
import json
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext
import threading

class VirtualShell:
    def __init__(self, vfs_path, log_path, script_path):
        self.vfs = {}  # Содержит виртуальную файловую систему
        self.current_dir = "/"
        self.log_path = log_path
        self.load_vfs(vfs_path)
        self.log = []
        self.script_path = script_path

    def log_action(self, action):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": action
        }
        self.log.append(entry)

    def save_log(self):
        with open(self.log_path, "w") as log_file:
            json.dump(self.log, log_file, indent=4)

    def load_vfs(self, zip_path):
        print(f"Loading VFS from: {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            for file in zip_file.namelist():
                self.vfs[file] = zip_file.read(file).decode('utf-8')

    def load_script(self):
        print(f"Loading script: {self.script_path}")
        try:
            with open(self.script_path, 'r') as script_file:
                for command in script_file:
                    print(f"Executing command from script: {command.strip()}")
                    self.execute(command.strip())
        except Exception as e:
            print(f"Error loading script: {e}")

    def execute(self, command):
        print(f"Command executed: {command}")
        parts = command.split()
        if not parts:
            return ""

        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            return self.ls()
        elif cmd == "cd":
            return self.cd(args)
        elif cmd == "wc":
            return self.wc(args)
        elif cmd == "rev":
            return self.rev(args)
        elif cmd == "uname":
            return self.uname()
        elif cmd == "exit":
            self.exit_shell()
        else:
            return f"Unknown command: {cmd}"

    def cd(self, args):
        if not args:
            return "cd: missing argument"
        path = args[0]

        print(f"Current directory before cd: {self.current_dir}")
        print(f"Requested path: {path}")

        # Обрабатываем относительные и абсолютные пути
        if not path.startswith("/"):
            path = self.current_dir.rstrip("/") + "/" + path
        if not path.endswith("/"):
            path += "/"

        if path not in self.vfs or self.vfs[path] is not None:  # Проверка существования директории
            return f"cd: no such directory: {args[0]}"

        self.current_dir = path
        print(f"Current directory after cd: {self.current_dir}")
        self.log_action(f"cd {args[0]}")
        return ""

    def ls(self):
        print(f"Current directory for ls: {self.current_dir}")
        print(f"VFS contents: {list(self.vfs.keys())}")

        # Показываем содержимое только текущей директории
        items = [
            key[len(self.current_dir):].split('/')[0] + ('/' if key.endswith('/') else '')
            for key in self.vfs
            if key.startswith(self.current_dir) and key != self.current_dir
        ]

        self.log_action("ls")
        return "\n".join(sorted(set(items)))

    def wc(self, args):
        if not args:
            return "wc: missing argument"
        path = args[0]
        print(f"Current directory for wc: {self.current_dir}")
        print(f"Requested path: {path}")

        # Создаём полный путь
        if not path.startswith("/"):
            path = self.current_dir.rstrip("/") + "/" + path

        if path not in self.vfs or self.vfs[path] is None:
            return f"wc: no such file: {args[0]}"

        content = self.vfs[path]
        lines = content.splitlines()
        words = sum(len(line.split()) for line in lines)
        chars = len(content)

        self.log_action(f"wc {args[0]}")
        return f"{len(lines)} {words} {chars}"

    def rev(self, args):
        if not args:
            return "rev: missing argument"
        path = args[0]
        print(f"Current directory for rev: {self.current_dir}")
        print(f"Requested path: {path}")

        # Создаём полный путь
        if not path.startswith("/"):
            path = self.current_dir.rstrip("/") + "/" + path

        if path not in self.vfs:
            return f"rev: no such file: {args[0]}"

        reversed_content = "\n".join(line[::-1] for line in self.vfs[path].splitlines())
        self.log_action(f"rev {args[0]}")
        return reversed_content

    def uname(self):
        self.log_action("uname")
        return "VirtualShell 1.0"

    def exit_shell(self):
        self.log_action("exit")
        self.save_log()
        sys.exit(0)

class ShellGUI:
    def __init__(self, shell):
        self.shell = shell
        self.root = tk.Tk()
        self.root.title("Virtual Shell")

        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=20)
        self.text_area.pack(padx=10, pady=10)
        self.text_area.insert(tk.END, "Virtual Shell started.\n")
        self.text_area.configure(state="disabled")

        self.entry = tk.Entry(self.root, width=80)
        self.entry.pack(padx=10, pady=5)
        self.entry.bind("<Return>", self.run_command)

    def run_command(self, event):
        command = self.entry.get()
        self.entry.delete(0, tk.END)

        output = self.shell.execute(command)

        self.text_area.configure(state="normal")
        self.text_area.insert(tk.END, f"$ {command}\n")
        if output:
            self.text_area.insert(tk.END, f"{output}\n")
        self.text_area.configure(state="disabled")
        self.text_area.see(tk.END)

    def run(self):
        print("Starting GUI...")
        self.root.mainloop()

if __name__ == "__main__":
    print("Program started")

    if len(sys.argv) < 4:
        print("Usage: python emulator.py <vfs.zip> <log.json> <script.sh>")
        sys.exit(1)

    vfs_path = sys.argv[1]
    log_path = sys.argv[2]
    script_path = sys.argv[3]

    shell = VirtualShell(vfs_path, log_path, script_path)

    # Запускаем выполнение скрипта в отдельном потоке
    def run_script():
        shell.load_script()

    script_thread = threading.Thread(target=run_script)
    script_thread.start()

    # Запускаем GUI в главном потоке
    gui = ShellGUI(shell)
    gui.run()
