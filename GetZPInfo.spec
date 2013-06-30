# -*- mode: python -*-
a = Analysis(['GetZPInfo.py'],
             pathex=['E:\\ledshow\\GetZPInfo'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'GetZPInfo.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True )
