import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import re

class BatchRenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频批量重命名工具")
        self.root.geometry("900x680")
        self.root.configure(bg='#f5f5f7')  # 现代背景色

        # 字体配置
        self.font_regular = ('Arial', 12)
        self.font_bold = ('Arial', 14, 'bold')
        self.font_small = ('Arial', 11)

        # 使用 ttk 样式
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f5f5f7')
        self.style.configure('TEntry', font=self.font_regular, borderwidth=0, focusthickness=3, focuscolor='none', padding=5)
        self.style.configure('TLabel', font=self.font_regular, background='#f5f5f7', foreground='#000000')
        self.style.configure('TText', font=self.font_regular, background='#ffffff', foreground='#000000', borderwidth=0, focusthickness=3, focuscolor='none')
        self.style.configure('TLabelframe', background='#f5f5f7', borderwidth=0, font=self.font_regular)
        self.style.configure('TLabelframe.Label', font=self.font_bold)

        # 文件夹路径框和按钮
        folder_frame = ttk.LabelFrame(root, text="选择文件夹", padding=10)
        folder_frame.pack(fill=tk.X, padx=20, pady=10)
        self.folder_path_var = tk.StringVar()
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path_var, width=60)
        self.folder_entry.pack(side=tk.LEFT, padx=5)
        self.select_folder_btn = tk.Button(folder_frame, text="浏览", command=self.select_folder, 
                                           font=self.font_bold, bg='#007aff', fg='white', 
                                           activebackground='#005bb5', activeforeground='white', 
                                           borderwidth=0, padx=10, pady=5)
        self.select_folder_btn.pack(side=tk.LEFT, padx=5)

        # 文件名与目标规则输入框
        self.file_vars = [tk.StringVar() for _ in range(4)]  # 当前文件名格式
        self.show_vars = [tk.StringVar() for _ in range(4)]  # 剧名输入框
        self.episode_vars = [tk.StringVar() for _ in range(4)]  # 集数变量输入框
        self.suffix_vars = [tk.StringVar() for _ in range(4)]  # 文件后缀显示框
        file_frame = ttk.LabelFrame(root, text="文件名格式", padding=10)
        file_frame.pack(fill=tk.X, padx=20, pady=10)
        for i in range(4):
            row_frame = ttk.Frame(file_frame)
            row_frame.pack(fill=tk.X, pady=5)
            ttk.Label(row_frame, text=f"文件 {i+1}:", width=10).pack(side=tk.LEFT, padx=5)
            ttk.Entry(row_frame, textvariable=self.file_vars[i], width=40, state='readonly').pack(side=tk.LEFT, padx=5)
            ttk.Entry(row_frame, textvariable=self.show_vars[i], width=15).pack(side=tk.LEFT, padx=5)
            ttk.Entry(row_frame, textvariable=self.episode_vars[i], width=10).pack(side=tk.LEFT, padx=5)
            ttk.Entry(row_frame, textvariable=self.suffix_vars[i], width=10, state='readonly').pack(side=tk.LEFT, padx=5)

        # 操作按钮
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)
        self.clear_btn = tk.Button(button_frame, text="清空", command=self.clear_fields, 
                                   font=self.font_bold, bg='#007aff', fg='white', 
                                   activebackground='#005bb5', activeforeground='white', 
                                   borderwidth=0, padx=10, pady=5)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        self.reset_btn = tk.Button(button_frame, text="回撤", command=self.reset_rename, 
                                   font=self.font_bold, bg='#007aff', fg='white', 
                                   activebackground='#005bb5', activeforeground='white', 
                                   borderwidth=0, padx=10, pady=5)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        self.confirm_btn = tk.Button(button_frame, text="确认", command=self.rename_files, 
                                     font=self.font_bold, bg='#007aff', fg='white', 
                                     activebackground='#005bb5', activeforeground='white', 
                                     borderwidth=0, padx=10, pady=5)
        self.confirm_btn.pack(side=tk.LEFT, padx=5)

        # 日志框
        log_frame = ttk.LabelFrame(root, text="日志", padding=10)
        log_frame.pack(fill=tk.BOTH, padx=20, pady=10, expand=True)
        self.log_text = tk.Text(log_frame, height=10, wrap=tk.WORD, font=self.font_regular, bg='#ffffff', fg='#000000', bd=0, highlightthickness=0)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # 常见视频和字幕后缀
        self.supported_suffixes = ('.mp4', '.mkv', '.avi', '.mov', '.flv', '.srt', '.ass', '.ssa' ,'.3gp', '.mpeg', '.wmv', '.mpg')

        # 用于记录重命名操作的日志
        self.rename_log = []

    # 其余方法保持不变

    def clear_fields(self):
        self.folder_path_var.set("")
        for var in self.file_vars + self.show_vars + self.episode_vars + self.suffix_vars:
            var.set("")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path_var.set(folder)
            self.auto_fill_file_names(folder)

    def auto_fill_file_names(self, folder):
        if not os.path.isdir(folder):
            self.log_message("选择的路径无效！")
            return

        try:
            files = [f for f in os.listdir(folder) if f.endswith(self.supported_suffixes)]
            name_groups = {}  # 存储不同命名格式的文件

            for file_name in files:
                prefix, ext = os.path.splitext(file_name)
                prefix = re.sub(r'(480p|720p|1080p|2K|4K|h265|h264|h263|MPEG-4)', '', prefix, flags=re.IGNORECASE)
                matches = list(re.finditer(r'(?<!\w)(E\d+|EP\d+|\d+)(?!\w)', prefix))
                numbered_pattern = prefix
                replacements = []

                for idx, match in enumerate(matches, start=1):
                    start, end = match.start(), match.end()
                    replacement = f"{{数字{idx}}}"
                    replacements.append((prefix[start:end], replacement))
                    numbered_pattern = numbered_pattern[:start] + replacement + numbered_pattern[end:]

                numbered_pattern += ext
                self.log_message(f"视频文件名：{file_name}，生成模式：{numbered_pattern}，替换详情：{replacements}")
                name_groups.setdefault(numbered_pattern, []).append((file_name, ext))

            for i, (pattern, group) in enumerate(name_groups.items()):
                if i < 4:  # 限制为4行
                    self.file_vars[i].set(pattern)
                    self.suffix_vars[i].set(group[0][1])  # 提取后缀
                    self.log_message(f"匹配的正则模式：{pattern}，文件示例：{group[0][0]}")

            if len(name_groups) == 0:
                self.log_message("该文件夹中没有找到支持的文件类型。")
            else:
                self.log_message(f"检测到 {len(name_groups)} 种文件名格式，已自动填充。")

        except Exception as e:
            self.log_message(f"自动填充文件名失败：{e}")

    def rename_files(self):
        folder = self.folder_path_var.get()
        if not folder or not os.path.isdir(folder):
            self.log_message("请选择有效的文件夹！")
            return

        try:
            renamed_count = 0
            self.rename_log = []  # 清空之前的记录
            for i, (pattern_var, show_var, episode_var, suffix_var) in enumerate(
                    zip(self.file_vars, self.show_vars, self.episode_vars, self.suffix_vars)):
                if pattern_var.get() and show_var.get() and episode_var.get():
                    show_name = show_var.get()
                    episode_var_name = episode_var.get().strip()
                    suffix = suffix_var.get()

                    if not re.fullmatch(r'数字\d+', episode_var_name):
                        self.log_message(f"第 {i + 1} 行集数变量输入无效，请输入格式如 '数字1'！")
                        continue

                    episode_index = int(episode_var_name.replace("数字", ""))
                    pattern = re.escape(pattern_var.get()).replace(r'\{数字' + str(episode_index) + r'\}', r'(\d+|E\d+|EP\d+)')

                    for file_name in os.listdir(folder):
                        match = re.match(pattern, file_name)
                        if match:
                            src = os.path.join(folder, file_name)
                            episode_match = match.group(1)
                            if episode_match.startswith("E") or episode_match.startswith("EP"):
                                episode_number = episode_match[1:] if episode_match.startswith("E") else episode_match[2:]
                            else:
                                episode_number = episode_match
                            episode_number = f"{int(episode_number):02d}"
                            new_name = f"{show_name}{episode_number}{suffix}"
                            dst = os.path.join(folder, new_name)
                            os.rename(src, dst)
                            renamed_count += 1
                            self.log_message(f"已重命名：{file_name} -> {new_name}")
                            self.rename_log.append((src, dst))  # 记录重命名操作
                        else:
                            self.log_message(f"未匹配：{file_name}")

            self.log_message(f"重命名完成，共处理 {renamed_count} 个视频。")
        except Exception as e:
            self.log_message(f"重命名失败：{e}")

    def reset_rename(self):
        if not self.rename_log:
            self.log_message("没有可撤销的重命名操作！")
            return

        try:
            for src, dst in reversed(self.rename_log):  # 逆序撤销
                os.rename(dst, src)
                self.log_message(f"已撤销：{os.path.basename(dst)} -> {os.path.basename(src)}")
            self.rename_log = []  # 清空日志
            self.log_message("所有重命名操作已撤销。")
        except Exception as e:
            self.log_message(f"撤销重命名失败：{e}")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = BatchRenameApp(root)
    root.mainloop()