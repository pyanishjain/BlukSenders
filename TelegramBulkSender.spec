# -*- mode: python -*-

block_cipher = None


a = Analysis(['TelegramBulkSender.py'],
             pathex=['C:\\Users\\ANISH JAIN\\Documents\\BulkSenders'],
             binaries=[('./driver/chromedriver.exe', './driver')],
             datas=[('./bot3.png', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='TelegramBulkSender',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='bot3.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='TelegramBulkSender')
