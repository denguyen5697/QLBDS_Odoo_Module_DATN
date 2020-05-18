from odoo import models, fields, api

class product(models.Model):
    _name = 'product.product'
    _inherit = 'product.product'

    location_apartment_number = fields.Char(string="Location/ Apartment Number", help="vị trí lô căn hộ của 1 nhà đó")
    parcel = fields.Char(string="Parcel", help="Số thửa của 1 miếng đất đó")
    project_id = fields.Many2one('project.project', string = "Project" , help="miếng đất này thuộc dự án nào")
    acreage = fields.Float(string = "Acreage", help="Diện tích của một mảnh đất")
    cart_id = fields.Many2one('customer.cart',
        ondelete='cascade', string="Course") 
    is_check = fields.Boolean(string = "Status(sold/ not sold)", help = "Sản phẩm đã giao cho đại lý đã được bán hay chưa?", default = False)    
    product_type = fields.Selection([
        ('1','Sản phẩm bán'),
        ('2','Sản phẩm mua'),
        ('3', 'Chi phí'),
        ('4','Tài sản'),
        ('5','Sản phẩm lưu kho'),
        ('6','Sản phẩm trang thiết bị'),
        ('7','Hóa đơn')
    ], string = 'Product Type', help = 'Loại sản phẩm', default = '1')    

# ------Trang thai giao dich cua san pham
    transaction_ids = fields.One2many('transaction.manager', 'product_id')
    transaction_id = fields.Many2one('transaction.manager', compute = 'transaction_compute')
    stage_name = fields.Selection(related = 'transaction_id.stage_name', store = True)

    color = fields.Integer(string = "Color"
                            , help="Màu sắc"
                            , compute = 'compute_color')
    def compute_color(self):
        for rec in self:
            color = 0
            if rec.stage_name == 'GS':
                color = 1
            elif rec.stage_name == 'GC':
                color = 2
            else: 
                color = 3
            rec.color = color
    @api.one 
    @api.depends('transaction_ids')
    def transaction_compute(self): 
        if len(self.transaction_ids) > 0:
            self.transaction_id = self.transaction_ids[0] 
            self.stage_name = self.transaction_id.stage_name
           

      
            

        

