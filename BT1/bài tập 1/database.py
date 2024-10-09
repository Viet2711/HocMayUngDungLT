# database.py

def export_data_to_txt(students, scores, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        for student in students:
            student_name = student[0]
            student_id = student[1]
            birth_year = student[2]
            score_info = scores.get(student_name, {'Math': 0, 'Literature': 0, 'English': 0})

            file.write(f"Tên: {student_name}, Mã số: {student_id}, Năm sinh: {birth_year}, "
                       f"Điểm Toán: {score_info['Math']}, Điểm Văn: {score_info['Literature']}, "
                       f"Điểm Anh: {score_info['English']}\n")

    print(f"Dữ liệu đã được xuất ra file {filename}.")

# Gọi hàm để xuất dữ liệu
if __name__ == "__main__":
    # Mô phỏng dữ liệu để xuất
    students = [("Nguyen Van A", "123456", "2000"), ("Tran Thi B", "654321", "1999")]
    scores = {
        "Nguyen Van A": {'Math': 8.5, 'Literature': 7.0, 'English': 9.0},
        "Tran Thi B": {'Math': 9.0, 'Literature': 8.5, 'English': 7.5}
    }
    export_data_to_txt(students, scores, "student_data.txt")