import unittest
from emulator import VirtualShell

class TestVirtualShell(unittest.TestCase):

    def setUp(self):
        # Создаем тестовую виртуальную файловую систему
        self.vfs = {
            "folder1/": None,
            "folder1/file1.txt": "This is file1 in folder1.",
            "folder2/": None,
            "folder2/file2.txt": "This is file2 in folder2.",
            "file3.txt": "This is a file in the root folder."
        }

        # Загружаем тестовую файловую систему вручную
        self.shell = VirtualShell("vfs.zip", "log.json", "script.sh")
        self.shell.vfs = self.vfs  # Загружаем тестовые данные
        self.shell.current_dir = "/"  # Устанавливаем текущую директорию

    def test_ls_root(self):
        print("Running test_ls_root...")
        output = self.shell.execute("ls")
        print(f"Output: {output}")
        expected = "folder1/\nfolder2/\nfile3.txt"
        self.assertEqual(output.strip(), expected)

    def test_cd_and_ls(self):
        print("Running test_cd_and_ls...")
        self.shell.execute("cd folder1")
        output = self.shell.execute("ls")
        print(f"Output: {output}")
        expected = "file1.txt"
        self.assertEqual(output.strip(), expected)

    def test_wc(self):
        print("Running test_wc...")
        output = self.shell.execute("wc folder1/file1.txt")
        print(f"Output: {output}")
        expected = "1 5 23"  # 1 строка, 5 слов, 23 символа
        self.assertEqual(output.strip(), expected)

    def test_rev(self):
        print("Running test_rev...")
        output = self.shell.execute("rev folder1/file1.txt")
        print(f"Output: {output}")
        expected = ".1redlof ni 1elif si sihT"  # Перевернутый текст
        self.assertEqual(output.strip(), expected)

    def test_uname(self):
        print("Running test_uname...")
        output = self.shell.execute("uname")
        print(f"Output: {output}")
        expected = "VirtualShell 1.0"
        self.assertEqual(output.strip(), expected)


if __name__ == "__main__":
    unittest.main()
