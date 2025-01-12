## Work from home VSL-2025 Write-up (Whitebox)

![image](https://github.com/user-attachments/assets/b23636c4-c4e6-402f-a7bd-5fcaa5ef94d6)
![image](https://github.com/user-attachments/assets/8d12c943-a0d1-4fb8-a46c-2e056cfb3d73)
![image](https://github.com/user-attachments/assets/ff07d630-6b50-4916-b1ff-3468448ac83a)

Trang web này có các chức năng như đăng nhập, đăng ký, quên mật khẩu.
Đầu tiên sẽ thử với tính năng đăng ký:
![image](https://github.com/user-attachments/assets/93fa3d82-f633-4653-8ff2-b6f6d21194cd)

Tại bài này, tài khoản và mật khẩu của người dùng không được lưu trong database mà được lưu dưới dạng folder và file:
![image](https://github.com/user-attachments/assets/45462211-08fe-40d9-98fd-3d3b5d4601a2)
![image](https://github.com/user-attachments/assets/6c3e90c0-9866-431e-b09e-4965421fd68a)
 
Mỗi khi đăng ký, nó sẽ tạo một folder là username trong folder home, còn password sẽ lưu vào một file tên password. Security question cũng được lưu dưới dạng file với tên file là câu hỏi trong folder questions, còn câu trả lời là nội dung trong file.
![image](https://github.com/user-attachments/assets/9a90f75d-7394-4831-ae40-543d9d2e605f)


Khi đăng nhập, nó sẽ kiểm tra tên folder username trong folder home, nếu có tồn tại thì user này có tồn tại, sau đó sẽ kiểm tra password so với file trong folder username ấy.
Chúng ta sẽ thử đăng ký một tài khoản:
![image](https://github.com/user-attachments/assets/1eea96cc-0e83-49d8-bca0-f71b89b14089)
![image](https://github.com/user-attachments/assets/0e902f2b-6b7d-4306-b4b7-54968aa7d5aa)

 
Khi đăng ký xong, tại thư mục home của web server sẽ xuất hiện username test1.
Bên trong có 1 folder là questions và password:
![image](https://github.com/user-attachments/assets/092db596-a6d0-44a3-b1e8-e3c398671295)
![image](https://github.com/user-attachments/assets/2c475874-192c-49ca-8f6a-679f3846de20)

 
Và bên trong folder questions:
![image](https://github.com/user-attachments/assets/06c240ed-2ebf-4ce6-a3b8-12d4e487b5db)
![image](https://github.com/user-attachments/assets/5ca77103-200f-4229-bdde-7e0de387b378)

Trang web còn có chức năng là forgot password:
![image](https://github.com/user-attachments/assets/12da6811-99ca-4d40-a28b-a90c0808bc1d)

Khi nhập username thì nó sẽ hiển thị ra các security question của tài khoản:
![image](https://github.com/user-attachments/assets/3401c194-3f52-4fe5-a959-9cf162daad6e)

Và nếu trả lời đúng thì sẽ hiển thị mật khẩu.
![image](https://github.com/user-attachments/assets/65b06bef-2845-4366-85cf-1d9bce89c106)

Vì flag sẽ xuất hiện khi đăng nhập admin, nên việc cần làm là làm thế nào để lấy được mật khẩu của admin.
Tại đây, trở lại với lúc đăng ký, khi lưu file security password, server không validate tên file mà sẽ lưu trực tiếp vào folder questions:
![image](https://github.com/user-attachments/assets/7e4d76af-b3fe-45ef-9e05-aa53bb031237)

Từ đây, chúng ta sẽ thử tạo một tài khoản mới rồi lưu security question ở thư mục cha bằng việc path traversal thử:
![image](https://github.com/user-attachments/assets/feb4d322-fbac-489d-b416-d53a66c736c6)
![image](https://github.com/user-attachments/assets/e34d7f9d-8648-4ac4-9052-d118501486e6)

 
Khi lưu lại thì quả thật file security question đã được lưu ra ngoài folder questions. Vì vậy, bây giờ chúng ta chỉ cần làm là ghi một security question vào trong folder admin, rồi dùng câu trả lời để lấy mật khẩu của admin.
![image](https://github.com/user-attachments/assets/0355c89e-3d8a-4c17-ab52-548c82025e1b)
![image](https://github.com/user-attachments/assets/9ff6d831-80f5-4868-8687-669e2aa66428)

 
Bây giờ tại folder admin đã có security question.
Chúng ta sẽ lấy mật khẩu của admin:
![image](https://github.com/user-attachments/assets/8003707b-07b8-4946-8183-feb86cfee9bc)
![image](https://github.com/user-attachments/assets/bf85981c-32e6-45b1-9f23-706871451f02)

 
Như vậy là đã lấy password của admin.
Đăng nhập vào admin sẽ có được flag:
![image](https://github.com/user-attachments/assets/01cffe78-b601-438f-ab1c-79ae2c499330)

