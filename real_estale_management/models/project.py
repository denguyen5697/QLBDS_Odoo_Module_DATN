from odoo import models, fields, api

class project(models.Model):
    _inherit = 'project.project'

    project_code = fields.Char(string="Code", required=True, help="mã dự án")
    project_location = fields.Char(string = "Location", help="Vị trí dự án")
    project_scale = fields.Char(string = "Scale", help="Dùng để diễn tả phạm vị 1 dự án(lớn/nhỏ/vừu) ")
    project_area = fields.Float(string = "Area", help="Dùng để diễn tả diện tích của 1 dự án: đơn vị m^2")
    project_status = fields.Selection([
        ('1','Chưa hoàn thành'),
        ('2','Đã hoàn thành')
    ], string = 'Project Status', help = 'Phản ánh tình trạng của 1 dự án', default = '1')
    type_projectId = fields.Many2one('typeproject', string = "Project Type", required=True, help='Loại dự án')
    price_project = fields.Float(string = "Price", help = "giá 1 dự án này là bao nhiêu")
    legal_id = fields.Many2one('legal', string ='Legal', required=True, help="Pháp lý cửa 1 dự án")
    project_scale = fields.Selection([('1', 'lớn'),('2','nhỏ'),('3','vừa')], default= '2', string="Project Scale", help = "Qui mô dự án")
    form_construction = fields.Many2one("form.construction", string = "Form Construction", help = "Hình thức xây dựng")
    discount = fields.Float(string = "Discount", help='Chiết khấu dự án')
    vendor_id = fields.Many2one('res.partner'
                                , string = 'Vendor/ Investor'
                                , help = 'Tên nhà cung cấp/ chủ đầu của dự án này'
                                , domain = [('supplier','=',True)])

    product_ids = fields.One2many('product.product', 'project_id')
    att = fields.Many2many('ir.attachment', string="Project Profile", help="Hồ sơ đính kèm đính kèm của dự án")
    project_investment = fields.Float(string="Investment", help="Vốn đầu tư")
    support_banks = fields.Many2many('res.bank'
                                , string = 'Support Bank'
                                , help = 'Ngân hàng hỗ trợ')
    color = fields.Integer(string = "Color"
                            , help="Màu sắc"
                            , compute='compute_color')
    def compute_color(self):
        for record in self:
            color = 0
            if record.project_status == '1':
                color = 1
            elif record.project_status == '2':
                color = 2         
            record.color = color                                                        


class TypeProject(models.Model):
    _name = 'typeproject'

    name = fields.Char(string="Name"
                        , help="tên của loại dự án"
                        , required = True)
    description = fields.Text(string = "Description", help="Mô tả loại dự án đó!")

class LegalProject(models.Model):
    _name = 'legal'

    legal_code = fields.Char(string = "Legal Code", required = True)
    name = fields.Char(string="name"
                        , help='Tên của pháp lý dự án'
                        , required = True)
    description = fields.Text(string = "Description", help="Mô tả pháp lý dự án đó!")

class form_construction(models.Model): 
    _name = "form.construction"

    name = fields.Char(string = "From Construction"
                        , help = "Hình thức xây dựng")


