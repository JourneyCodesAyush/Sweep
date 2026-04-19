# cli.spec
a = Analysis(
    ['src/sweep/__main__.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('src/sweep', 'sweep'),  # include package files
    ],
    hiddenimports=['sweep', 'importlib.metadata'],
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    name='sweep',
    console=True,
    onefile=True,
)