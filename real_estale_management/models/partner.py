from odoo import models, fields, api

class MyContact(models.Model):
    # Ingerit from Res Partner
    _name = "res.partner"
    _inherit = 'res.partner'


    type_partner = fields.Selection([('1', 'Đối tác phụ'),('2','Đối tác chính')], default= '2')
    agency = fields.Boolean(string='Is a agency', default=False,
                               help="Kiểm tra xem có phải là nhà cung cấp hay không")
    ward = fields.Char(help='Phường')
    district = fields.Char(help='Quận')                           

    model2_ids = fields.One2many('contract', 'customer_id', string='Models 2')
    # contract customer information (Party A)
    identify_card=fields.Char(string='Identity Card Number')
    date_identity_card= fields.Date(string="Date",help="Ngày cấp chứng minh nhân dân") 
    place_of_issue=fields.Char(string="Place of issue",help="Nơi cấp chứng minh nhân dân")
    model3_ids = fields.One2many('contract', 'customer_id1', string='Models 3')
    
    # contract party B information
    registered_address = fields.Char(string = 'Registered Address',help= "Trụ sở của công ty")
    # tax_code = fields.Char(string = 'Tax code',help = "Mã số thuế")                           
