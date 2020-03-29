# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
block_cipher = None


datas_dir = [('C:/Users/drarn/Documents/Code/Study/Kivy/kivy_venv/Lib/site-packages', '.'),
(r'C:\Users\drarn\Documents\Code\Study\Kivy\Something\windows\*.kv','windows'),
(r'C:\Users\drarn\Documents\Code\Study\Kivy\Something\personalUtilities\*.png','.\personalUtilities'),
(r'C:\Users\drarn\Documents\Code\Study\Kivy\Something\personalUtilities\BaseDeDatos.db','.\personalUtilities')]


a = Analysis(scripts = ['main.py'],
             pathex=['C:\\Users\\drarn\\Documents\\Code\\Study\\Kivy\\Something'],
             binaries=[],
             datas=datas_dir,
             hiddenimports=['pkg_resources.py2_warn'],
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
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               Tree('windows\\'),
               Tree('personalUtilities\\'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
