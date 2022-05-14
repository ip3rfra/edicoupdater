# -*- mode: python ; coding: utf-8 -*-
import datetime
import PyInstaller.config

block_cipher = None


bd = datetime.datetime.now()
bdiso = bd.isoformat()
bddir = bd.strftime("%m-%d-%Y_%H%M%S")

PyInstaller.config.CONF['distpath'] = f"./dist/{bddir}"

# Write version info into _constants.py resource file
with open("src/_constants.py", 'w') as f:
    f.write('author = "Ip3rFra"\n')
    f.write(f'buildDate = "{bdiso}"')
    
a = Analysis(
    ['src/main.py', 'src/strings.py', 'src/_constants.py'],
    pathex=[],
    binaries=[],
    datas=[('res/icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='EdicoUpdater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='metadata.rc',
    icon = 'res/icon.ico',
)
