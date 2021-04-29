from dmai.dm import DM
from dmai.ui import UserInterface

def start():
    '''Initialise the DM and load the required data'''
    dm = DM()
    dm.load()
    return dm
    
def run(dm: DM):
    '''Run the DM via CLI'''
    ui = UserInterface(dm)
    ui.execute()