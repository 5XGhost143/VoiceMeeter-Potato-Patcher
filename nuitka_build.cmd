python -m nuitka ^
    --onefile ^
    --windows-disable-console ^
    --enable-plugin=tk-inter ^
    --include-module=pymem ^
    --include-data-file=config.json=config.json ^
    --output-dir=build ^
    --output-filename=Patcher.exe ^
    main.py
