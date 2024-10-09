from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import database
from database import *

# Khởi tạo cửa sổ
win = Tk()
win.title("Quản Lý Sinh Viên")

# Tạo Notebook để chứa các tab
notebook = ttk.Notebook(win)
notebook.pack(pady=10, expand=True)

# Tạo tab chính
main_tab = Frame(notebook)
notebook.add(main_tab, text="Quản Lý Sinh Viên")

# Tạo tab mới
new_tab = Frame(notebook)
notebook.add(new_tab, text="Quản Lý Điểm")

# biến rõng lưu dũ liệu sinh viên
students = []#bao gồm tên, mssv, năm sinh
scores = {}# bao gôm tên sinh viên và điểm của sinh viên đó

# Hàm thêm sinh viên
def add_student():
    student_name = name_entry.get()
    student_id = id_entry.get()
    birth_year = birth_year_entry.get()
    
    if student_name and student_id and birth_year:
        student_info = f"{student_name} - {student_id} - {birth_year}"
        students.append((student_name, student_id, birth_year))
        listbox.insert(END, student_info)
        update_student_list()  # Cập nhật danh sách sinh viên trong tab 2
        name_entry.delete(0, END)
        id_entry.delete(0, END)
        birth_year_entry.delete(0, END)
    else:
        messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin")

# Hàm sửa sinh viên
def edit_student():
    selected_index = listbox.curselection()#chọn sinh viên để sửa
    if selected_index:
        student_name = name_entry.get()
        student_id = id_entry.get()
        birth_year = birth_year_entry.get()
        
        if student_name and student_id and birth_year:
            listbox.delete(selected_index)
            updated_info = f"{student_name} - {student_id} - {birth_year}"
            students[selected_index[0]] = (student_name, student_id, birth_year)
            listbox.insert(selected_index, updated_info)
            update_student_list()  # Cập nhật danh sách sinh viên trong tab 2
            name_entry.delete(0, END)
            id_entry.delete(0, END)
            birth_year_entry.delete(0, END)
        else:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin")
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để sửa")

# Hàm xóa sinh viên
def delete_student():
    selected_index = listbox.curselection()
    if selected_index:
        listbox.delete(selected_index)
        del students[selected_index[0]]  # Xóa sinh viên từ danh sách
        update_student_list()  # Cập nhật danh sách sinh viên trong tab 2
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để xóa")

# Hàm cập nhật danh sách sinh viên trong tab 2
def update_student_list():
    student_listbox.delete(0, END)  # Xóa tất cả các mục trong Listbox
    for student in students:
        student_info = f"{student[0]} - {student[1]} - {student[2]}"
        student_listbox.insert(END, student_info)

# Hàm nhập điểm cho sinh viên
def enter_scores():
    selected_index = student_listbox.curselection()
    if selected_index:
        student_name = students[selected_index[0]][0]  # Lấy tên sinh viên
        math_score = math_entry.get()
        literature_score = literature_entry.get()
        english_score = english_entry.get()

        # Kiểm tra xem điểm có hợp lệ không
        try:
            math_score = float(math_score)
            literature_score = float(literature_score)
            english_score = float(english_score)
        except ValueError:
            messagebox.showwarning("Thông báo", "Vui lòng nhập điểm hợp lệ.")
            return

        # Lưu điểm vào từ điển scores cho sinh viên được chọn
        scores[student_name] = {
            'Math': math_score,
            'Literature': literature_score,
            'English': english_score
        }

        # Cập nhật danh sách điểm trong Listbox
        update_student_scores_listbox()

        messagebox.showinfo("Thông báo", f"Điểm đã được nhập cho {student_name}!\nĐiểm: Toán: {math_score}, Văn: {literature_score}, Anh: {english_score}")
        # Xóa nội dung trong các Entry sau khi nhập điểm
        math_entry.delete(0, END)
        literature_entry.delete(0, END)
        english_entry.delete(0, END)
    else:
        messagebox.showwarning("Thông báo", "Vui lòng chọn sinh viên để nhập điểm")

# Hàm cập nhật danh sách sinh viên và điểm của họ trong Listbox
def update_student_scores_listbox():
    student_listbox.delete(0, END)  # Xóa tất cả các mục trong Listbox
    for student in students:
        student_name = student[0]
        score_info = scores.get(student_name, {'Math': 0, 'Literature': 0, 'English': 0})
        total_score = sum(score_info.values())
        
        # Hiển thị tổng điểm và điểm từng môn
        student_listbox.insert(END, f"{student_name} - Tổng điểm: {total_score} - Toán: {score_info['Math']}, Văn: {score_info['Literature']}, Anh: {score_info['English']}")

# Hàm sắp xếp sinh viên theo điểm cao nhất
def sort_by_scores():
    sorted_students = sorted(scores.items(), key=lambda x: sum(x[1].values()), reverse=True)
    student_listbox.delete(0, END)  # Xóa tất cả các mục trong Listbox
    for student in sorted_students:
        student_listbox.insert(END, f"{student[0]} - Tổng điểm: {sum(student[1].values())}")

# Hàm lọc điểm cao nhất theo môn học
def highest_score_by_subject():
    highest_scores = {}
    for student, score in scores.items():
        for subject, value in score.items():
            if subject not in highest_scores or value > highest_scores[subject][1]:
                highest_scores[subject] = (student, value)
                messagebox.showinfo("Điểm cao nhất", "\n".join([f"{subject}: {info[0]} với điểm {info[1]}" for subject, info in highest_scores.items()]))

def export_data():
    filename = "students_data.txt"  # Tên file xuất ra
    database.export_data_to_txt(students, scores, filename)

# Tạo Label tiêu đề cho tab quản lý sinh viên
title_label = Label(main_tab, text="ỨNG DỤNG QUẢN LÝ SINH VIÊN", fg="red", font="helvetica", width=30)
title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Tạo Listbox để hiển thị danh sách sinh viên
listbox = Listbox(main_tab, width=50, height=10)
listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Tạo Entry để nhập tên sinh viên
name_label = Label(main_tab, text="Nhập tên Sinh Viên:")
name_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

name_entry = Entry(main_tab, width=40)
name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Tạo Entry để nhập mã số sinh viên
id_label = Label(main_tab, text="Nhập mã số Sinh Viên:")
id_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

id_entry = Entry(main_tab, width=40)
id_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Tạo Entry để nhập năm sinh sinh viên
birth_year_label = Label(main_tab, text="Nhập năm sinh Sinh Viên:")
birth_year_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

birth_year_entry = Entry(main_tab, width=40)
birth_year_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Tạo các Button nằm ngang nhau trên cùng một dòng và có kích thước đồng đều
button_frame = Frame(main_tab)
button_frame.grid(row=5, column=0, columnspan=3, pady=10)

add_button = Button(button_frame, text="Thêm", command=add_student, width=10)
add_button.grid(row=0, column=0, padx=5)

edit_button = Button(button_frame, text="Sửa", command=edit_student, width=10)
edit_button.grid(row=0, column=1, padx=5)

delete_button = Button(button_frame, text="Xóa", command=delete_student, width=10)
delete_button.grid(row=0, column=2, padx=5)

# Cấu hình lưới để giãn nở Listbox
main_tab.grid_rowconfigure(1, weight=1)
main_tab.grid_columnconfigure(1, weight=1)

# Tab quản lý điểm
scores_title_label = Label(new_tab, text="QUẢN LÝ ĐIỂM SINH VIÊN", fg="blue", font="helvetica", width=30)
scores_title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

student_listbox = Listbox(new_tab, width=60, height=10)
student_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Tạo Label và Entry cho các môn học
math_label = Label(new_tab, text="Nhập điểm Toán:")
math_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

math_entry = Entry(new_tab, width=20)
math_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

literature_label = Label(new_tab, text="Nhập điểm Văn:")
literature_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
literature_entry = Entry(new_tab, width=20)
literature_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

english_label = Label(new_tab, text="Nhập điểm Anh:")
english_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")

english_entry = Entry(new_tab, width=20)
english_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Tạo các Button nằm ngang nhau trên cùng một dòng và có kích thước đồng đều cho tab điểm
scores_button_frame = Frame(new_tab)
scores_button_frame.grid(row=5, column=0, columnspan=3, pady=10)

enter_scores_button = Button(scores_button_frame, text="Nhập Điểm", command=enter_scores, width=10)
enter_scores_button.grid(row=0, column=0, padx=5)

sort_scores_button = Button(scores_button_frame, text="Sắp Xếp Điểm", command=sort_by_scores, width=10)
sort_scores_button.grid(row=0, column=1, padx=5)

highest_score_button = Button(scores_button_frame, text="Điểm Cao Nhất", command=highest_score_by_subject, width=10)
highest_score_button.grid(row=0, column=2, padx=5)

export_button = Button(scores_button_frame, text="Xuất Dữ Liệu", command=export_data, width=20)
export_button.grid(row=0, column=3, padx=5)

# Cấu hình lưới để giãn nở Listbox
new_tab.grid_rowconfigure(1, weight=1)
new_tab.grid_columnconfigure(1, weight=1)

# Chạy ứng dụng
win.mainloop()