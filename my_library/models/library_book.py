# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    active = fields.Boolean(default=True)
    author_ids = fields.Many2many('res.partner', string='Authors')
    state = fields.Selection(
        [('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')],
        'State', default="available")
    cost_price = fields.Float('Book Cost')
    category_id = fields.Many2one('library.book.category')

    def make_available(self):
        self.ensure_one()
        self.state = 'available'

    def make_borrowed(self):
        self.ensure_one()
        self.state = 'borrowed'

    def make_lost(self):
        self.ensure_one()
        self.state = 'lost'

class ResPartner(models.Model):
    _inherit = 'res.partner'
    authored_book_ids = fields.Many2many('library.book', string='Authored Books')
    count_books = fields.Integer('',
        compute='_compute_count_books'
    )

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)
