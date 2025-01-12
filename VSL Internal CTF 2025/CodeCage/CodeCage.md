## CodeCage VSL-2025 Write-up (Whitebox)

![image](https://github.com/user-attachments/assets/f58b739c-6745-49fe-b125-ba20f9ae6b12)

Trong bài này, chúng ta sẽ làm việc với một sandbox cho phép thực thi các lệnh Python mà người dùng nhập vào thông qua giao diện web. Ví dụ:
![image](https://github.com/user-attachments/assets/7ecec816-da42-4d4f-b2d4-81dd6ede07b5)
![image](https://github.com/user-attachments/assets/4ef63f83-324f-4be8-9342-2d244d815a52)
 
Tuy nhiên không phải lệnh nào cũng có thể thực hiện được. Tại source code có thể thấy whitelist những module được phép sử dụng và blacklist những hàm không được sử dụng:
![image](https://github.com/user-attachments/assets/ea8aac42-d618-4c46-8841-6344e8acd8bd)
![image](https://github.com/user-attachments/assets/2568f473-8449-41f7-b7e2-3531bf3506ee)
 
Flag được lưu ở cùng web folder nên chúng ta sẽ thử nhập một hàm để mở flag:
![image](https://github.com/user-attachments/assets/8481d0a2-26f2-4cac-a26a-7d599d7fef15)
![image](https://github.com/user-attachments/assets/063226ee-f463-49ad-8cab-dcd9c4e1d137)
 
Có thể thấy rằng nó không cho phép dùng hàm open trong khi hầu như các hàm đọc file đều là hàm open.
Tuy nhiên, tại các module được phép có module là pathlib để xử lý đường dẫn tệp và thư mục.
![image](https://github.com/user-attachments/assets/71a1e999-387c-4d22-8ebd-0968382cacb8)

Chúng ta có thể dùng module này để đọc file từ module này.
![image](https://github.com/user-attachments/assets/1033340e-41c3-40f9-bb2f-946a328e433d)

Chỉ với vài dòng đơn giản như vậy là chúng ta đã lấy được flag:
![image](https://github.com/user-attachments/assets/18542c8a-1699-4179-bd8f-4d9ca2e02f16)

