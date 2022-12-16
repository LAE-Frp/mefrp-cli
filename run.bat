@echo off
color 2F

echo 欢迎使用 mefrp-cli v1.0
echo By kingc
echo.
echo Mirror Edge Frp 服务即将启动...
echo 下方出现 start proxy success 即为隧道启动成功
frpc.exe -c temp/%1%
