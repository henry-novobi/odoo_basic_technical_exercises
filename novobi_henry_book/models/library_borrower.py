from email.policy import default
from odoo import models, fields, api

class LibraryBorrower(models.TransientModel):
    _name = "library.borrower"
    _description = "Library Borrower"

    borrower_id = fields.Many2one("res.partner", required = True)
    book = fields.Char("Book", readonly = True)
    ISBN = fields.Char("ISBN", readonly = True)
    return_date = fields.Date("Borrower Date", required = True)

    # @api.model
    # def default_get(self, fields_list):
    #     print("D________V_________VVV________")
    #     defaults = super(LibraryBorrower, self).default_get(fields_list)
    #     return defaults

    
    def write_Borrower(self):
        self.ensure_one()
        store = self.env["library.book"].search([('ISBN','=',self.ISBN)])
        if store and self.borrower_id:
            store.write({"current_borrower_id": self.borrower_id, "date_return": self.return_date, "status": "borrowed"})
            # store.write({"message_ids": "Change to Borrowed Status"})
        return {'type': 'ir.actions.act_window_close'}

    # @api.depends('borrower_ids.current_borrower_id')
    # def _compute_Borrower(self):
    #     print("Computed__________________", self.borrower_ids)
    #     self.borrower_ids = self.env['library.book'].search([('current_borrower_id', '=', self.borrower_ids)])






