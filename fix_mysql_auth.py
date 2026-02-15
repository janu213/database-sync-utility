import pymysql

# We need to connect as root first, but we can't if auth fails.
# However, usually the issue is from external clients (pymysql). 
# If we can't connect, we need to run SQL inside the container.

print("Please run the following command in your terminal to fix MySQL authentication:")
print("docker exec -it mysql_target mysql -u root -prootpassword -e \"ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'rootpassword'; FLUSH PRIVILEGES;\"")
