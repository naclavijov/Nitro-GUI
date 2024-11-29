# -*- mode: python ; coding: utf-8 -*-
# This is a specification file for compiling the application into a single folder

block_cipher = None


a = Analysis(['server.py'],
             pathex=['D:\\GUI-Nitro-11-12-24\\src'],
             binaries=[],
             datas=[
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/dash_iconify','dash_iconify'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/dash_mantine_components','dash_mantine_components'), 
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/dash_bootstrap_components','dash_bootstrap_components'), 
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/dash_bootstrap_templates','dash_bootstrap_templates'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/dash_daq','dash_daq'), 
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/plotly','plotly'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/dash','dash'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/joblib','joblib'),
	       ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/psutil','psutil'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/dash','dash'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/numpy','numpy'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/pandas','pandas'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/statsmodels','statsmodels'),
	       ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/kaleido','kaleido'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/scipy','scipy'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/matplotlib','matplotlib'),
               ('C:/Users/nacla/anaconda3/envs/PyenvSENAI/Lib/site-packages/openpyxl','openpyxl'),


               ('D:/GUI-Nitro-11-12-24/src/assets','assets'),
               ('D:/GUI-Nitro-11-12-24/src/Backend','Backend'),
               ('D:/GUI-Nitro-11-12-24/src/components','components'),
               ('D:/GUI-Nitro-11-12-24/src/utils','utils'),

               ('D:/GUI-Nitro-11-12-24/src/app.py','.'),
               ('D:/GUI-Nitro-11-12-24/src/index.py','.'),


                  
                  ],
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
          name='launch_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          icon = 'assets/icons/icon.ico',
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='app')
