# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Tic_tac_2_online.py'],
             pathex=['C:\\Users\\kaipa\\PycharmProjects\\KVT\\myprojects\\experiments\\Pygames\\Tic_Tac_2_exe'],
             binaries=[],
             datas=[],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Tic_tac_2_online',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='Tic_tac_2_icon1.ico')
