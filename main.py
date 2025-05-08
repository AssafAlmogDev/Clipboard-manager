import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class PDFToolkit(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PDF Toolkit")
        self.geometry("600x400")
        self.resizable(False, False)

        self.tabview = ctk.CTkTabview(self, width=580, height=360)
        self.tabview.pack(pady=20)

        self.merge_tab = self.tabview.add("Merge PDFs")
        self.split_tab = self.tabview.add("Split PDF")

        self.pdf_files = []
        self.setup_merge_tab()
        self.setup_split_tab()

    def setup_merge_tab(self):
        self.merge_listbox = ctk.CTkTextbox(self.merge_tab, width=540, height=200)
        self.merge_listbox.pack(pady=10)

        btn_frame = ctk.CTkFrame(self.merge_tab)
        btn_frame.pack(pady=10)

        add_btn = ctk.CTkButton(btn_frame, text="Add PDFs", command=self.add_pdfs)
        add_btn.pack(side="left", padx=10)

        merge_btn = ctk.CTkButton(btn_frame, text="Merge and Save", command=self.merge_pdfs)
        merge_btn.pack(side="left", padx=10)

    def setup_split_tab(self):
        self.split_label = ctk.CTkLabel(self.split_tab, text="No file selected")
        self.split_label.pack(pady=10)

        select_btn = ctk.CTkButton(self.split_tab, text="Select PDF", command=self.select_split_pdf)
        select_btn.pack(pady=5)

        self.page_range_entry = ctk.CTkEntry(self.split_tab, placeholder_text="Page range (e.g., 1-3)")
        self.page_range_entry.pack(pady=5)

        split_btn = ctk.CTkButton(self.split_tab, text="Split and Save", command=self.split_pdf)
        split_btn.pack(pady=10)

        self.split_file = None

    def add_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for f in files:
            if f not in self.pdf_files:
                self.pdf_files.append(f)
                self.merge_listbox.insert("end", f + "\n")

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("No PDFs", "Please add PDF files to merge.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")],
                                                 title="Save Merged PDF")
        if not save_path:
            return

        merger = PdfMerger()
        try:
            for pdf in self.pdf_files:
                merger.append(pdf)
            merger.write(save_path)
            merger.close()
            messagebox.showinfo("Success", f"Merged PDF saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def select_split_pdf(self):
        file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file:
            self.split_file = file
            self.split_label.configure(text=os.path.basename(file))

    def split_pdf(self):
        if not self.split_file:
            messagebox.showwarning("No PDF", "Please select a PDF to split.")
            return

        page_range = self.page_range_entry.get().strip()
        if '-' not in page_range:
            messagebox.showerror("Invalid Range", "Please use the format: 1-3")
            return

        try:
            start, end = map(int, page_range.split('-'))
            reader = PdfReader(self.split_file)
            writer = PdfWriter()

            for i in range(start - 1, end):
                writer.add_page(reader.pages[i])

            save_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                     filetypes=[("PDF files", "*.pdf")],
                                                     title="Save Split PDF")
            if save_path:
                with open(save_path, "wb") as f:
                    writer.write(f)
                messagebox.showinfo("Success", f"Split PDF saved to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = PDFToolkit()
    app.mainloop()
