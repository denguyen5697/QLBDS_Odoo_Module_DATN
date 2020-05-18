# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api

class transaction_manager(models.Model):
    _name = 'transaction.manager'

    name = fields.Char(string="Name"
                                    , required = True
                                    , help = "Tên giao dịch")
    stage_name = fields.Selection([
        ('GS', 'Giữ số'),
        ('GC', 'Giữ chỗ'),
        ('DC', 'Đặt cọc'),
    ], default='GS'
    , required = True
    , string="Stage Name"
    , help = "Trình tự giao dịch hiện tại")

    next_stage = fields.Selection([        
        ('GC', 'Giữ chỗ'),
        ('DC', 'Đặt cọc'),
        ], default='GC'
        , required = True 
        , string="Next Stage"
        , help = "Trình tự kế tiếp của giao dịch")

    product_id = fields.Many2one('product.product'
                                , string="Product"
                                , help = "Sản phẩm"
                                , compute = 'load_product_and_customer')
    customer_id = fields.Many2one('res.partner',string="Customer"
                                , help = "Tên khách hàng"
                                , domain="[('customer', '=', True)]"
                                , compute = 'load_product_and_customer')
    sale_order_id = fields.Many2one('sale.order'
                                , domain="[('is_agency','=', False)]")                            
    expired_date = fields.Date(string="Expiration Date"
                                , help = "Ngày kết thúc giao dịch")
    pay_amount = fields.Float(string = "Payment amount", help="Số tiền thanh toán")
    status = fields.Selection([
        ('CHT', 'Chưa hoàn thành'),
        ('Open', 'Đã hoàn thành'),
        ('Closed', 'Không còn hiệu lực')
    ], string="Transaction Status", help = "Trạng thái giao dịch", default='CHT')
    description = fields.Text('Notes')
    

    @api.model
    def check_expired_transaction(self):
        print("Đang vào kiểm tra trạng thái giao dịch!!")
        current_date = datetime.now().date()
        for rec in self.search([('status', '!=', 'Closed')]):
            if rec.expired_date < current_date and rec.status != 'Open':
                rec.write({'status': 'Closed'})
                print("Trạng thái giao dịch đã hủy bỏ")

    @api.onchange('stage_name')
    def onchange_stage_name(self):
        print("ONCHANGE - stage name ....Đã vào!")
        for record in self:
            print("stage_name", record.stage_name)
            if record.stage_name == 'GS':
                print("1::")
                record.next_stage = 'GC'
            elif record.stage_name == 'GC':
                print("2::")
                record.next_stage = 'DC'

    @api.onchange('sale_order_id')
    def load_product_and_customer(self):
        print("Đã vào onchange mở bán...")
        for rec in self:
            # print("khách hàng", rec.sale_order_id.partner_id, ", Sản phẩm: ", rec.sale_order_id.order_line.product_id) 
            rec.customer_id = rec.sale_order_id.partner_id.id
            rec.product_id = rec.sale_order_id.order_line.product_id.id                  


