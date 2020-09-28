import logging

from enhancer.tasks.operator import Operator
from processes.click import Click
from processes.wait import Wait

class Destructor(Operator):

    def __init__(self, config, inventory):
        super().__init__(config, inventory)
        self.log = logging.getLogger('enhancer')
        self.destruct_button = self.config['assets']['destructor']['button_of_start']
        self.dx, self.dy = self.destruct_button
        self.dx, self.dy = int(self.dx), int(self.dy)
        # import pdb; pdb.set_trace()

    def proceed(self):
        self.destroy()
        self.log.info('End destruction')
    
    def destroy(self):
        while len(self.inventory.working_cells):
            self.log.info('Destructor items {0}'.format(len(self.inventory.working_cells)))
            for cell in self.inventory.working_cells[:20]:
                x, y = self.finder.point(cell.center())
                Click(x,y, 'double').make_click()
                Wait(0.2).delay()
            
            x, y = self._get_destruct_point()
            Click(x,y, 'double').make_click()
            Wait(2).delay()

            self.update_inventory()
            self.log.info('Destructor rest items {0}'.format(len(self.inventory.working_cells)))
        
    def update_inventory(self):
        self.inventory.open_source()
        self.inventory.update_grid()
        self.inventory.set_params()
    
    def _get_destruct_point(self):
        entry = self.inventory.grid.entry
        x,y = self.finder.point(entry)
        return self.dx + x, self.dy + y