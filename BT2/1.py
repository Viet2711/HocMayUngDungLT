import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Thông tin kết nối cơ sở dữ liệu PostgreSQL
DB_HOST = "localhost"
DB_NAME = "1"
DB_USER = "postgres"
DB_PASS = "27112002"

def connect_db():
    """Kết nối đến cơ sở dữ liệu PostgreSQL."""
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối đến cơ sở dữ liệu: {e}")
        return None

def load_students():
    """Tải danh sách sinh viên từ cơ sở dữ liệu."""
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách sinh viên: {e}")
            return []

def add_student():
    """Thêm sinh viên mới vào cơ sở dữ liệu."""
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    major = major_entry.get()

    # Kiểm tra dữ liệu đầu vào
    if not name or not age or not gender or not major:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showwarning("Cảnh báo", "Tuổi phải là số nguyên!")
        return

    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)", (name, age, gender, major))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Thông báo", "Thêm sinh viên thành công!")
            clear_entries()
            refresh_student_list()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể thêm sinh viên: {e}")

def update_student():
    """Cập nhật thông tin sinh viên."""
    try:
        selected_item = student_list.selection()[0]
        student_id = student_list.item(selected_item)['values'][0]
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để cập nhật!")
        return

    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    major = major_entry.get()

    # Kiểm tra dữ liệu đầu vào
    if not name or not age or not gender or not major:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showwarning("Cảnh báo", "Tuổi phải là số nguyên!")
        return

    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s", (name, age, gender, major, student_id))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Thông báo", "Cập nhật sinh viên thành công!")
            clear_entries()
            refresh_student_list()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật sinh viên: {e}")

def delete_student():
    """Xóa sinh viên khỏi cơ sở dữ liệu."""
    try:
        selected_item = student_list.selection()[0]
        student_id = student_list.item(selected_item)['values'][0]
    except IndexError:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên để xóa!")
        return

    if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?"):
        conn = connect_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Thông báo", "Xóa sinh viên thành công!")
                clear_entries()
                refresh_student_list()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xóa sinh viên: {e}")

def clear_entries():
    """Xóa nội dung các trường nhập liệu."""
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    gender_entry.delete(0, tk.END)
    major_entry.delete(0, tk.END)

def refresh_student_list():
    """Tải lại danh sách sinh viên và hiển thị trên giao diện."""
    for i in student_list.get_children():
        student_list.delete(i)
    for student in load_students():
        student_list.insert("", tk.END, values=student)

# Tạo cửa sổ giao diện chính
window = tk.Tk()
window.title("Quản lý Sinh viên")

# Tạo các nhãn và trường nhập liệu
name_label = ttk.Label(window, text="Tên:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = ttk.Entry(window)
name_entry.grid(row=0, column=1, padx=5, pady=5)

age_label = ttk.Label(window, text="Tuổi:")
age_label.grid(row=1, column=0, padx=5, pady=5)
age_entry = ttk.Entry(window)
age_entry.grid(row=1, column=1, padx=5, pady=5)

gender_label = ttk.Label(window, text="Giới tính:")
gender_label.grid(row=2, column=0, padx=5, pady=5)
gender_entry = ttk.Entry(window)
gender_entry.grid(row=2, column=1, padx=5, pady=5)

major_label = ttk.Label(window, text="Ngành học:")
major_label.grid(row=3, column=0, padx=5, pady=5)
major_entry = ttk.Entry(window)
major_entry.grid(row=3, column=1, padx=5, pady=5)

# Tạo các nút chức năng
add_button = ttk.Button(window, text="Thêm sinh viên", command=add_student)
add_button.grid(row=4, column=0, padx=5, pady=5)

update_button = ttk.Button(window, text="Cập nhật thông tin", command=update_student)
update_button.grid(row=4, column=1, padx=5, pady=5)

delete_button = ttk.Button(window, text="Xóa sinh viên", command=delete_student)
delete_button.grid(row=5, column=0, padx=5, pady=5)

refresh_button = ttk.Button(window, text="Tải lại danh sách", command=refresh_student_list)
refresh_button.grid(row=5, column=1, padx=5, pady=5)

# Tạo danh sách sinh viên với Treeview
columns = ("ID", "Tên", "Tuổi", "Giới tính", "Ngành học")
student_list = ttk.Treeview(window, columns=columns, show="headings")
for col in columns:
    student_list.heading(col, text=col)
student_list.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Tải danh sách sinh viên ban đầu
refresh_student_list()

window.mainloop()