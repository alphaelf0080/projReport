"""
網路連線診斷工具
用於診斷後端服務的網路配置和連接問題
"""
import socket
import subprocess
import sys
import platform
from pathlib import Path

def print_section(title):
    """列印章節標題"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_success(msg):
    """列印成功訊息"""
    print(f"✅ {msg}")

def print_error(msg):
    """列印錯誤訊息"""
    print(f"❌ {msg}")

def print_warning(msg):
    """列印警告訊息"""
    print(f"⚠️  {msg}")

def print_info(msg):
    """列印資訊訊息"""
    print(f"ℹ️  {msg}")

def get_local_ip():
    """獲取本機 IP"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return hostname, local_ip
    except Exception as e:
        return None, None

def check_port_listening(port):
    """檢查 port 是否正在監聽"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result == 0

def check_http_connection(url, timeout=5):
    """檢查 HTTP 連接"""
    try:
        import requests
        response = requests.get(url, timeout=timeout)
        return True, response.status_code, response.json()
    except ImportError:
        return False, None, "requests 模組未安裝"
    except Exception as e:
        return False, None, str(e)

def check_firewall_rules():
    """檢查防火牆規則（僅 Windows）"""
    if platform.system() != "Windows":
        return None
    
    try:
        result = subprocess.run(
            ['netsh', 'advfirewall', 'firewall', 'show', 'rule', 'name=all'],
            capture_output=True,
            text=True,
            encoding='big5',
            errors='ignore'
        )
        
        # 搜尋 3010 相關規則
        rules_found = []
        lines = result.stdout.split('\n')
        current_rule = {}
        
        for line in lines:
            if '規則名稱:' in line or 'Rule Name:' in line:
                if current_rule and '3010' in str(current_rule):
                    rules_found.append(current_rule)
                current_rule = {'name': line.split(':', 1)[1].strip()}
            elif '啟用:' in line or 'Enabled:' in line:
                current_rule['enabled'] = line.split(':', 1)[1].strip()
            elif 'LocalPort' in line or '本機連接埠:' in line:
                current_rule['port'] = line.split(':', 1)[1].strip()
        
        return rules_found
    except Exception as e:
        return None

def list_network_interfaces():
    """列出所有網路介面"""
    try:
        import psutil
        interfaces = {}
        for interface, addrs in psutil.net_if_addrs().items():
            ipv4_addrs = [addr.address for addr in addrs if addr.family == socket.AF_INET]
            if ipv4_addrs:
                interfaces[interface] = ipv4_addrs
        return interfaces
    except ImportError:
        return None

def main():
    """主診斷函數"""
    PORT = 3010
    
    print_section("🔍 網路連線診斷工具")
    print(f"目標 Port: {PORT}")
    
    # 1. 系統資訊
    print_section("📋 系統資訊")
    print(f"作業系統: {platform.system()} {platform.release()}")
    print(f"Python 版本: {sys.version.split()[0]}")
    
    # 2. 網路配置
    print_section("🌐 網路配置")
    hostname, local_ip = get_local_ip()
    if hostname and local_ip:
        print_success(f"主機名稱: {hostname}")
        print_success(f"本機 IP: {local_ip}")
    else:
        print_error("無法獲取本機 IP")
    
    # 列出所有網路介面
    interfaces = list_network_interfaces()
    if interfaces:
        print_info("所有網路介面:")
        for iface, addrs in interfaces.items():
            for addr in addrs:
                print(f"   • {iface}: {addr}")
    
    # 3. Port 檢查
    print_section(f"🔌 Port {PORT} 檢查")
    if check_port_listening(PORT):
        print_success(f"Port {PORT} 已開啟（後端正在運行）")
    else:
        print_error(f"Port {PORT} 未開啟（後端未啟動）")
        print_warning("請執行: python main_gemini.py")
    
    # 4. HTTP 連接測試
    print_section("🌐 HTTP 連接測試")
    
    # 測試 localhost
    print("測試 localhost...")
    success, status, data = check_http_connection(f"http://localhost:{PORT}/api/health")
    if success:
        print_success(f"本機連接成功 (HTTP {status})")
        print(f"   回應: {data}")
    else:
        print_error(f"本機連接失敗: {data}")
    
    # 測試 IP
    if local_ip:
        print(f"\n測試 IP ({local_ip})...")
        success, status, data = check_http_connection(f"http://{local_ip}:{PORT}/api/health")
        if success:
            print_success(f"IP 連接成功 (HTTP {status})")
            print(f"   回應: {data}")
        else:
            print_error(f"IP 連接失敗: {data}")
    
    # 5. 防火牆檢查 (Windows only)
    if platform.system() == "Windows":
        print_section("🛡️  防火牆規則檢查")
        rules = check_firewall_rules()
        
        if rules is None:
            print_error("無法檢查防火牆規則（需要管理員權限）")
        elif len(rules) == 0:
            print_error(f"未找到 port {PORT} 的防火牆規則")
            print_warning("請以管理員身份執行:")
            print(f'   netsh advfirewall firewall add rule name="Backend {PORT}" dir=in action=allow protocol=TCP localport={PORT}')
        else:
            print_success(f"找到 {len(rules)} 條相關防火牆規則:")
            for rule in rules:
                print(f"   • {rule.get('name', 'Unknown')}")
                if 'enabled' in rule:
                    print(f"     啟用: {rule['enabled']}")
    
    # 6. 建議配置
    print_section("📝 建議的前端配置")
    if local_ip:
        print(f"const BACKEND_SERVER_IP = '{local_ip}';")
        print(f"const BACKEND_PORT = {PORT};")
        print(f"const API_BASE = 'http://{local_ip}:{PORT}';")
    
    # 7. 測試命令
    print_section("🧪 測試命令")
    print("本機測試:")
    print(f"   curl http://localhost:{PORT}/api/health")
    if local_ip:
        print(f"\nIP 測試:")
        print(f"   curl http://{local_ip}:{PORT}/api/health")
        print(f"\n遠端連接測試 (在遠端主機上執行):")
        print(f"   Test-NetConnection -ComputerName {local_ip} -Port {PORT}")
        print(f"   curl http://{local_ip}:{PORT}/api/health")
    
    # 8. 檢查清單
    print_section("✅ 檢查清單")
    checklist = [
        (check_port_listening(PORT), f"後端服務在 port {PORT} 運行"),
        (success if 'success' in locals() else False, "本機 HTTP 連接成功"),
        (rules and len(rules) > 0 if rules is not None else None, "防火牆規則已設定"),
    ]
    
    for status, item in checklist:
        if status is True:
            print_success(item)
        elif status is False:
            print_error(item)
        elif status is None:
            print_warning(f"{item} (無法檢查)")
    
    print("\n" + "=" * 70)
    print("診斷完成！")
    print("=" * 70)

if __name__ == "__main__":
    main()
