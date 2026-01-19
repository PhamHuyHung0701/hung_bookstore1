-- Script cập nhật mật khẩu thành plain text
-- Chạy script này trong MySQL để cập nhật dữ liệu mẫu

USE bookstore_db;

-- Cập nhật mật khẩu cho các customer hiện có thành plain text
UPDATE customers SET password = '123456' WHERE email = 'nguyenvana@example.com';
UPDATE customers SET password = '123456' WHERE email = 'tranthib@example.com';
UPDATE customers SET password = '123456' WHERE email = 'levanc@example.com';

-- Hoặc xóa và insert lại dữ liệu mẫu với mật khẩu plain text
-- DELETE FROM cart_items;
-- DELETE FROM carts;
-- DELETE FROM customers;

-- INSERT INTO customers (name, email, password) VALUES
-- ('Nguyen Van A', 'nguyenvana@example.com', '123456'),
-- ('Tran Thi B', 'tranthib@example.com', '123456'),
-- ('Le Van C', 'levanc@example.com', '123456');

-- Kiểm tra kết quả
SELECT id, name, email, password FROM customers;
