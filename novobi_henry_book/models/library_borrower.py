from email.policy import default
from odoo import models, fields, api

class LibraryBorrower(models.TransientModel):
    _name = "library.borrower"
    _description = "Library Borrower"

    borrower_ids = fields.One2many("library.book", "current_borrower_id", string="Borrower", store="True",
                                   computed='_compute_Borrower', required=True, default=lambda self: self.env.current_borrower_id)
    # return_date = fields.Many2one("library.book")
    books = fields.Many2one("library.book", default=lambda self: self._context.get('ISBN'))

    # @api.model
    # def default_get(self, fields_list):
    #     print("D________V_________VVV________")
    #     defaults = super(LibraryBorrower, self).default_get(fields_list)
    #     if 'borrower_ids' in fields_list:
    #         # task_default = self.env['library.book'].with_context(fsm_mode=True).default_get(['borrower_ids'])
    #         # self.borrower_ids = task_default.get('borrower_ids', False)
    #         # print("_________________________MODEL",self.borrower_ids)
    #         # defaults.update({'borrower_ids': task_default.get('borrower_ids', False)})
    #         defaults['books'] = self._context.get('ISBN')
            
    #         # defaults['borrower_ids'] = self._context.get('current_borrower_id')
    #     return defaults


    @api.depends('borrower_ids.current_borrower_id')
    def _compute_Borrower(self):
        print("Computed__________________", self.borrower_ids)
        self.borrower_ids = self.env['library.book'].search([('current_borrower_id', '=', self.borrower_ids)])






