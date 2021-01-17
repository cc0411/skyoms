# 安装初始化包，uwsgi需要该依赖
```
yum install libffi-devel
```

# 安装mysql
## 下载
```
wget https://downloads.mysql.com/archives/get/file/mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz
```
## 解压
```
tar xvf mysql-5.7.20-linux-glibc2.12-x86_64.tar.gz -C /usr/local/
```
## 制作软链接
```
ln -s /usr/local/mysql-5.7.20-linux-glibc2.12-x86_64/ /usr/local/mysql
```
## 创建用户
```
useradd -r -s /sbin/nologin -M mysql
```
## 授权
```
chown -R mysql:mysql /usr/local/mysql
mkdir -p /data/mysql/
chown -R mysql:mysql /data/mysql/
```
##配置环境变量
```
vim /etc/profile

export PATH=$PATH:/usr/local/mysql/bin

source /etc/profile
```
## 初始化
```
mysqld --initialize-insecure --user=mysql --basedir=/usr/local/mysql --datadir=/data/mysql/
```
## 配置文件my.cnf
见conf下的my.cnf  4G内存相关配置

##制作启动文件

```
vim /etc/systemd/system/mysqld.service
```

见conf下的mysqld.service

## 开机自动启动mysql
```
systemctl start mysqld
systemctl enable mysqld
```
## 配置密码
```
mysqladmin -uroot -p password 123456
```
## 创建表 
```
create database  skyoms  charset utf8；
```

------------------------------------------------------------
# 安装redis
## 解压
tar xvf redis-5.0.8.tar.gz  -C /usr/local/
## 制作软连接
```
cd /usr/local/
ln -s redis-5.0.8/ redis
```
## 编译
```cd redis
make
cd src/
make install
```
## 配置文件
mkdir /etc/redis
见conf下的redis.conf
## 开机启动文件
见conf下的redis.service
## 开机启动
```
systemctl start redis
systemctl enable redis
```
## 测试连接
```redis-cli -h 127.0.0.1
auth  Redis@123
```
---------------------------------------------------------------------
# 安装pcre
##解压
```
tar xvf pcre-8.44.tar.gz 
```
##编译安装
```
cd pcre-8.44/
./configure  --prefix=/usr/local/pcre
make
make install
```
----------------------------------------------------------------------
# 安装nginx
## 创建启动用户
```
useradd -r -s /sbin/nologin -M nginx
```
## 解压
```
tar xvf nginx-1.14.2.tar.gz 
```
## 编译安装
```
cd nginx-1.14.2/
./configure --user=nginx --group=nginx --prefix=/usr/local/nginx --with-http_stub_status_module --with-http_ssl_module --with-stream --with-http_gzip_static_module --with-http_sub_module
make
make install
```
## 制作启动文件
vim /etc/systemd/system/nginx.service
见conf下的nginx.service
## 配置文件
cd /usr/local/nginx/
见conf下的nginx.conf skyoms.conf
## 启动nginx
```
systemctl start nginx
systemctl enable nginx
```
---------------------------------------------------------------------------
# 安装node
## 解压
```
tar xvf node-v14.14.0-linux-x64.tar.xz -C /usr/local/
```
##安装
```
cd /usr/local/
ln -s node-v14.14.0-linux-x64/ node
vi /etc/profile
export PATH=$PATH:/usr/local/node/bin
source /etc/profile
```
## 查看
node -v

---------------------------------------------------------------------------------
# 安装python
## 解压
```
tar xvf Python-3.8.6.tgz 
```
##编译安装
```
cd Python-3.8.6/
./configure --prefix=/usr/local/python3.8
make &&make install
```
添加命令到bin下
```
cd /usr/local/python3.8/bin/
cp pip3 /usr/bin/
cp python3 /usr/bin/
```

--------------------------------------------------------------------------------------
# 安装virtuenv和uwsgi
联网下直接使用pip装，或者pypi网上下载
## 创建一个虚拟python
```
virtualenv  --python=python3.8  venv
```
## 制作uwsgi文件
见conf下的uwsgi.ini
##启动
uwsgi --ini   uwsgi.ini 
##重载
uwsgi --reload uwsgi/uwsgi.pid 
##停止
uwsgi --stop uwsgi/uwsgi.pid 

------------------------------------------------------------------------------------------
#安装celery和django-celery-beat
联网下直接使用pip装，或者pypi网上下载
## 制作celery.conf和service启动文件
见conf下
## 启动
systemctl start celery
systemctl status  celery
systemctl start celerybeat
systemctl status  celerybeat

-----------------------------------------------------------------------------------------------
# 收集静态文件
```
npm run build
rm -rf static/*
python manage.py collectstatic 
``` 

# 上线后删除所有d2-admin配置中关于VUE_APP_API和 process.env.VUE_APP_BASE_API 相关内容，然后执行build


# 监控cpu和内存
```
安装psutil
设置客户端crontab定时任务
* * * * * python /opt/client/cpu.py
* * * * * python /opt/client/memory.py
```