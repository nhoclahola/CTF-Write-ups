UserPortal VSL-2025 Write-up (Whitebox)
![image](https://github.com/user-attachments/assets/3876792f-ee9f-487f-8d9a-89706709dd5c)

Bài này ngay khi đi vào chỉ có chức năng đăng nhập mà không có đăng ký:
![image](https://github.com/user-attachments/assets/25187b42-5ea9-4641-b9d0-75d27166ec27)

Đầu tiên chúng ta sẽ xem qua source code.
Khi khởi tạo bảng thì sẽ tạo một người dùng là admin:
![image](https://github.com/user-attachments/assets/177ab849-6b2c-4837-bb6c-f6c0f71a09ab)

Tại chức năng đăng nhập, code xử lý theo kiểu dùng trực tiếp lệnh SQL nối chuỗi.
![image](https://github.com/user-attachments/assets/f3321e97-3bd6-4ccc-b93b-6231fcb31b66)

Vì vậy chúng ta có thể sử dụng SQL Injection để truy cập vào tài khoản admin (Do chỉ có 1 tài khoản):
![image](https://github.com/user-attachments/assets/f9eaa105-a4cc-45c8-9031-bc4125f0dc90)
![image](https://github.com/user-attachments/assets/6f5963a8-3423-4718-9ef9-d2a4fc8252c7)

Tại tài khoản, chúng ta sẽ có thêm 2 trang là Profile và Feedback:
![image](https://github.com/user-attachments/assets/01f407d4-0aaf-4720-b549-82413b7f86a2)
![image](https://github.com/user-attachments/assets/e68e1a95-cd7c-4ed1-b1b5-75c79d740e15)

Tại mã nguồn FeedbackController.php:
![image](https://github.com/user-attachments/assets/64537a69-7cb3-4e6c-a6d3-bb506168c144)

Chúng ta thấy rằng nó sẽ lấy giá trị feedback từ HTTP Post và sử dụng hàm render_template để lấy ra output để xem có thành công hay không.
Tại hàm render_template:
![image](https://github.com/user-attachments/assets/51cf52ac-381f-4bdc-860c-cc598323b93a)
![image](https://github.com/user-attachments/assets/148c2921-ca8c-40e3-ac47-32f840cbec38)
 
Tại hàm feedback sử dụng blacklist để kiểm tra và dùng eval để thực thi giá trị feedback từ đầu vào. Vì vậy cần chú ý ở hàm eval vì nó sẽ thực thi code php, đây là tiền đề để chúng ta tấn công template injection.
![image](https://github.com/user-attachments/assets/13225b33-325a-4514-b997-5578f477f327)

Sau đó render ra trang feedback từ file feedback ở phần view, nếu thành công hay thất bại thì sẽ có thông báo trên đầu:
![image](https://github.com/user-attachments/assets/4885fe14-2367-4dee-bf64-58d10a0bd855)

Chúng ta sẽ thử tạo một feedback:
![image](https://github.com/user-attachments/assets/3c2382fa-3efd-43f4-9d5a-89f0965d9035)
![image](https://github.com/user-attachments/assets/86ec4b6a-d4d9-455e-9ab0-ab461692ab7d)

 
Thử nhập giá trị tại blacklist:
![image](https://github.com/user-attachments/assets/18e82b6e-2e84-4577-a9b5-55286feffed0)
![image](https://github.com/user-attachments/assets/e15850eb-29a4-438f-bcba-344e5a82a493)

 
Trong php có hàm readfile không nằm trong blacklist, chúng ta sẽ dùng hàm readfile để đọc file flag và dùng $ để lấy giá trị đó cho hàm eval khi nãy đọc:
![image](https://github.com/user-attachments/assets/1dd0c949-1688-4df0-85bc-92b81febfa5c)

readfile() là hàm PHP đọc file và in trực tiếp nội dung ra output, nó trả về số byte đọc được. Tuy nhiên, nó sẽ in nội dung file trước khi trả về số bytes. Vì vậy nó sẽ in ra flag ở đầu trang.
Và như vậy là đã có được flag.


