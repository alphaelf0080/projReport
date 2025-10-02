"""
測試安裝是否成功
"""
import sys

print("=" * 70)
print("🔍 檢查依賴安裝狀態")
print("=" * 70)

# 檢查必要套件
required_packages = {
    'fastapi': 'FastAPI',
    'uvicorn': 'Uvicorn',
    'pydantic': 'Pydantic',
    'torch': 'PyTorch',
    'diffusers': 'Diffusers',
    'transformers': 'Transformers',
    'PIL': 'Pillow',
    'cv2': 'OpenCV',
    'sklearn': 'scikit-learn',
    'numpy': 'NumPy',
    'loguru': 'Loguru'
}

failed = []
success = []

for module, name in required_packages.items():
    try:
        __import__(module)
        version = __import__(module).__version__ if hasattr(__import__(module), '__version__') else 'N/A'
        print(f"✅ {name:20} - v{version}")
        success.append(name)
    except ImportError:
        print(f"❌ {name:20} - 未安裝")
        failed.append(name)

print("\n" + "=" * 70)

if failed:
    print(f"❌ 失敗：{len(failed)} 個套件未安裝")
    print(f"   {', '.join(failed)}")
    print("\n請執行：pip3 install -r requirements-macos.txt")
    sys.exit(1)
else:
    print(f"✅ 成功：所有 {len(success)} 個套件已正確安裝！")
    
# 檢查 PyTorch 後端
print("\n" + "=" * 70)
print("🔥 PyTorch 後端檢查")
print("=" * 70)

try:
    import torch
    print(f"PyTorch 版本: {torch.__version__}")
    print(f"CUDA 可用: {torch.cuda.is_available()}")
    print(f"CUDA 版本: {torch.version.cuda if torch.cuda.is_available() else 'N/A'}")
    
    # 檢查 MPS (Apple Silicon)
    if hasattr(torch.backends, 'mps'):
        print(f"MPS (Metal) 可用: {torch.backends.mps.is_available()}")
        if torch.backends.mps.is_available():
            print("✅ 可使用 Apple Silicon GPU 加速！")
        else:
            print("⚠️  將使用 CPU 運算（較慢）")
    else:
        print("⚠️  此版本不支援 MPS，將使用 CPU 運算")
        
    print(f"CPU 執行緒數: {torch.get_num_threads()}")
    
except Exception as e:
    print(f"❌ PyTorch 檢查失敗: {e}")

print("\n" + "=" * 70)
print("✅ 安裝檢查完成！")
print("=" * 70)
print("\n📋 下一步：")
print("   python3 main.py  # 啟動後端服務")
print("=" * 70)
