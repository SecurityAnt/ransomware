# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['C:\\Users\\user\\PycharmProjects\\ransomware\\final.py'],
             pathex=['C:\\Users\\user\\PycharmProjects\\ransomware\\final'],
	 binaries=[],
             datas=[('ui/*.png','ui'),('ui/*.gif','ui')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ransomware_fast',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
