from odoo import models, fields, api
class Status_Product(models.Model):
     _name= 'contract'
     
     
     # Contract Information
     contract_id = fields.Char(string= "Contract Number",required="True")
     name = fields.Char(string= "Contract Name"
                         , required = True)
     product_id = fields.Many2one('product.product',string="Product",require='True')
     project_rel = fields.Many2one(related='product_id.project_id',string='Project')
     date_start = fields.Date(string="Date Signed"
                              , help = 'Ngày kí hợp đồng' )
     status = fields.Selection([('1', 'Đã kí'),('2','Đã duyệt'),('3','Chờ duyệt')], default= '2', string="Status", help = "Tình trạng của hợp đồng")
     deposit = fields.Float(string="Deposit"
                              , help = 'Số tiền đặt cọc' )
     signed = fields.Boolean('Signed', default=True)
     not_signed = fields.Boolean('Approved',default = True)
     
     # Customer Information (Party A)
     customer_id = fields.Many2one('res.partner',string= "Party A", required='True',domain="[('customer', '=', True)]")
     customer_street = fields.Char(related='customer_id.street', string='Permanent Address')
     customer_date=fields.Date(related='customer_id.date',string='Days of birth')
     customer_sreet2 = fields.Char(related='customer_id.street2',string ='Contact Address')
     customer_email = fields.Char(related = 'customer_id.email',string = 'Email')
     customer_phone = fields.Char(related = 'customer_id.phone',string = 'Phone Number')
     customer_identity = fields.Char(related = 'customer_id.identify_card')
     customer_date_identity = fields.Date(related = 'customer_id.date_identity_card')
     customer_place_of_issue = fields.Char(related = 'customer_id.place_of_issue')
     
     # Party B Information
     customer_id1 = fields.Many2one('res.partner',string='Party B',required='True',domain="[('supplier','=',True),('is_company', '=', True)]")
     representative = fields.Many2one('res.partner',string='Representative')
     company_address = fields.Char(related = 'customer_id1.registered_address')
     company_taxcode = fields.Char(related = 'customer_id1.vat')
     representative_pos = fields.Char(related = 'representative.function')
     company_phone = fields.Char(related = 'customer_id1.phone',string = 'Tel',help = "Số điện thoại")
     description=fields.Text(string='Description')
     
     #Annex
     annex_id = fields.Many2many('contract_annex',string = 'Contract Annex')
     
     #transaction status
     # trans_id = fields.Many2many('transaction_status',string = 'Transaction Status')
     # trans_id = fields.Char(string = 'Status ID',help = 'Mã giao dịch sản phẩm')
     # trans_name = fields.Char(string ='Thông tin giao dịch')
     # trans_date = fields.Date(string = 'Ngày giao dịch')
     status_id = fields.Many2many('transaction_status',string = 'Information Payment')

     color = fields.Integer(string = "Color"
                            , help="Màu sắc"
                            , compute='compute_color')
     def compute_color(self):
        for record in self:
            color = 0
            if record.status == '1':
                color = 1
            elif record.status == '2':
                color = 2  
            elif record.status == '3':
                color = 3             
            record.color = color # xuất report
     @api.multi
     def print_contract(self):
          print("====>>>>  Da vao In")
          # self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

          return self.env.ref('customer.action_report_contract')\
            .with_context(discard_logo_check=True).report_action(self)
            
     @api.multi
     def print_contract_pdf(self):
          return self.env.ref('customer.action_report_contract').report_action(self)
     
class ContractAnnex(models.Model):
     _name = 'contract_annex'
     annex_id = fields.Char(string = 'Annex Contract ID',help = 'Mã phụ lục của hợp đồng')
     name_annex = fields.Char(string = 'Annex Contract ID Name',help = 'Tên điều khoản')
     description_annex = fields.Text(string = 'Content',help = 'Nội dung điều khoản')
     
class Transaction_status(models.Model):
      _name = 'transaction_status'
      trans_id = fields.Char(string = 'Payment times',help = 'Đợt thanh toán')
      trans_price = fields.Char(string ='Price',help='Tổng số tiền product')
      trans_date = fields.Date(string = 'Date of payment',help='Ngày thanh toán')
      arrears= fields.Char(string='Arrears',help='Số tiền còn lại của product')
      paid= fields.Char(string='Paid',help='Đã thanh toán')
      content=fields.Text(string='Content',help='Ghi chú')
   
     
# representative=fields.Many2one(related='customer_id1.parent_id')
@api.onchange('customer_id1')
def onchange_cus_id(self):  
     for record in self:
          if record.customer_id1:
               return {'domain': {'representative': [('customer_id1', '=', record.customer_id1.parent_name)]}}
          else:
               return {'domain':{'representative':[]}}



          
        
     
     


     
     
        
    
    
    
    

