def execFile(programName):
    with open(programName) as f:
        code = compile(f.read(), '', 'exec')
        exec(code)
        

execFile('battleship.py')
