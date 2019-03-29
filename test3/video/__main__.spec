# -*- mode: python -*-

block_cipher = None


a = Analysis(['__main__.py'],
             pathex=['CacheManager.py', 'Downloader.py', 'CacheVideoView.py', 'VideoModel.py', 'DownManagerView.py', 'VideoView.py', 'request.py', '/Users/iyunshu/Desktop/Python/test3/video'],
             binaries=[],
             datas=[],
             hiddenimports=['video'],
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
          name='__main__',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='__main__')
