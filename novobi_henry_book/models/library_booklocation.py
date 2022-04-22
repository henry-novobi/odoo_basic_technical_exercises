from odoo import models, fields, api, exceptions


class LibraryBookLocation(models.Model):
    _name = 'library.booklocation'
    _description = 'Library Book Location'

    name = fields.Char('Name')
    book_ids = fields.One2many('library.book', 'ISBN', string = "Books")
    total_available_books = fields.Integer('Total Available Book', compute='_compute_total_book')

    # Rule: do not use sql constraint
    # _sql_constraints = [
    # ('name', 'unique(name)', 'Duplicate Book Location Name')
    # ]

    @api.constrains('name')
    def _check_name(self):
        self.ensure_one()
        # loc_counts = self.search_count([('name', '=', self.name)])
        loc_counts = self.env['library.booklocation'].search([('name', '=', self.name), ('id', '!=', self.id)])
        print(loc_counts)
        if loc_counts:
            raise exceptions.ValidationError("Location already exists!")

    # @api.depends('book_ids')
    def _compute_total_book(self):
        for record in self:
            record.total_available_books = record.env['library.book'].search_count([('location_id', '=', record.name)])
