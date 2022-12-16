import json
import os
import sys

import requests
from rich import print

import config
import ini_operation


def init():
    print(config.logo)
    print(config.version)
    print("[cyan]By kingc[/cyan]\n")
    print("[bold cyan]1)[/bold cyan] [cyan]设置Token[/cyan]")
    print("[bold cyan]2)[/bold cyan] [cyan]扫描隧道并打印[/cyan]")
    print("[bold cyan]3)[/bold cyan] [cyan]选择隧道并下载配置文件[/cyan]")
    print("[bold cyan]4)[/bold cyan] [cyan]选择配置文件并启动隧道[/cyan]")
    print("[bold cyan]5)[/bold cyan] [cyan]清除软件缓存以节省空间[/cyan]")
    print("[bold cyan]6)[/bold cyan] [cyan]退出软件[/cyan]\n")


def main():
    choice = int(input("请选择: "))
    if choice == 1:
        token = input("请输入Token(https://api.laecloud.com): ")
        ini_operation.setToken(token)
        print("[bold green]设置成功! 请重启软件![/bold green]")
        input("请按回车键继续...")
        sys.exit()
    elif choice == 2:
        response = requests.get("https://api.laecloud.com/api/modules/frp/hosts", headers=headers)
        response.encoding = response.apparent_encoding
        json_response = json.loads(response.text)
        if len(json_response["data"]) == 0:
            print("[red]目前您的账户没有隧道[/red]")
        else:
            for i in range(0, len(json_response["data"])):
                print(f"[bold white]{i+1}[/bold white] [bold cyan]{json_response['data'][i]['name']}[/bold cyan]")
        input("请按回车键继续...")
    elif choice == 3:
        id = int(input("请输入隧道ID (程序输出的ID): "))
        response = requests.get("https://api.laecloud.com/api/modules/frp/hosts?with_config=1", headers=headers)
        response.encoding = response.apparent_encoding
        json_response = json.loads(response.text)
        if len(json_response["data"]) == 0:
            print("[red]目前您的账户没有隧道![/red]")
        else:
            try:
                with open(f"temp/{json_response['data'][id-1]['name']}.ini", 'w', encoding="UTF-8") as f:
                    f.write(json_response["data"][id-1]["config"]["server"]+"\n"+json_response["data"][id-1]["config"]["client"])
                print("[bold green]下载成功![/bold green]")
            except FileNotFoundError:
                os.mkdir("temp")
                with open(f"temp/{json_response['data'][id-1]['name']}.ini", 'w', encoding="UTF-8") as f:
                    f.write(json_response["data"][id-1]["config"]["server"]+"\n"+json_response["data"][id-1]["config"]["client"])
                print("[bold green]下载成功![/bold green]")
        input("请按回车键继续...")
    elif choice == 4:
        inis = os.listdir("temp")
        if len(inis) == 0:
            print("[bold red]您尚未下载配置文件![/bold red]")
        else:
            for i in range(0, len(inis)):
                print(f"[bold white]{i+1}[/bold white] [bold cyan]{inis[i]}[/bold cyan]")
            id = int(input("请输入配置文件ID (程序输出的ID): "))
            os.system(f"start run.bat {inis[id-1]}")
        input("请按回车键继续...")
    elif choice == 5:
        inis = os.listdir("temp")
        if len(inis) == 0:
            print("[bold red]您尚未下载配置文件![/bold red]")
        else:
            for i in range(0, len(inis)):
                os.remove(f"temp/{inis[i]}")
            os.rmdir("temp")
            print("[bold green]清理成功![/bold green]")
        input("请按回车键继续...")
    elif choice == 6:
        sys.exit()
    else:
        print("[bold red]您的输入不合法[/bold red]")
        input("请按回车键继续...")


if __name__ == '__main__':
    ini_operation.init()
    headers = {
        "authorization": f"Bearer {ini_operation.readToken()}"
    }
    while True:
        init()
        main()
