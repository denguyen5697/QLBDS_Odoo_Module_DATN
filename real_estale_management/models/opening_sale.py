# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions
from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, ValidationError

class opening_sale(models.Model):
    # _name = 'customer.customer'
    _name = "customer.opening.sale"
    _description = 'opeing sale'

    name = fields.Char(string = 'Name', help = 'Tên đợt mở bán', required = True)   
    start_date = fields.Datetime(string = 'Start Date'
                            , help= 'Ngày bắt đầu của đợt mở bán đó'
                            , default=fields.Datetime.now
                            , required=True)
    end_date = fields.Datetime(string = 'End Date'
                            , help = 'Ngày kết thúc đợt mở bán đó'
                            , default=fields.Datetime.now
                            , required=True) 
    agency_id = fields.Many2many('res.partner'
                                , string = 'Agency'
                                , help='Những đại lý trong đợt mở bán đó'
                                , required = True
                                , domain="[('agency', '=', True)]")
    cart_id = fields.Many2one('customer.cart', compute = 'compute_cart', inverse='cart_inverse')
    cart_ids = fields.One2many('customer.cart', 'opening_saleId')
    product_id = fields.Many2many('product.product'
                                , string = 'Products'
                                , help = 'Danh sách sản phảm thuộc giỏ hàng'
                                , domain="[('is_check', '=', False)]" )
    _sql_constraints=[
        ('date_check', "CHECK ( (start_date <= end_date))", "Ngày bắt đầu phải nhỏ ngày kết thúc!")
    ]                            

    
    def your_button(self):
        print("da vao",self.id)
        "Your Code"
        context = {
            'default_opening_saleId': self.id,
            'default_start_date': self.start_date,
            'default_end_date': self.end_date,            
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'customer.cart',    # name of respective model,
            'target': 'new',
            'context': context,
        }

    # @api.multi
    # @api.constrains('endDate', 'startDate')
    # def date_constrains(self):

    #           for rec in self:

    #                   if rec.endDate < rec.startDate:
    #                       raise exceptions.ValidationError('Sorry, End Date Must be greater Than Start Date...')
    #                     #    raise (_('Sorry, End Date Must be greater Than Start Date...'))
   
    # @api.onchange('endDate', 'startDate')
    # def _verify_valid_date_opening_sale(self):
    #     for record in self:
    #         if record.endDate < record.startDate:
    #             return {
    #                 'warning': {
    #                     'title': "Giá trị 'date' không chính xác",
    #                     'message': "Ngày bắt đầu mở bán phải nhỏ hơn ngày kết thúc",
    #                 },
    #             }
        
    @api.one
    @api.depends('cart_ids')
    def compute_cart(self):
        if len(self.cart_ids) > 0:
            self.cart_id = self.cart_ids[0]

    @api.one
    def cart_inverse(self):
        if len(self.cart_ids) > 0:
            # delete previous reference
            cart = self.env['customer.cart'].browse(self.cart_ids[0].id)
            cart.opening_saleId = False
        # set new reference
        self.cart_id.opening_saleId = self   
        
class cart(models.Model):
    _name = "customer.cart"
    _description = 'cart'

    cart_code = fields.Char(string = 'Cart Code', help = 'Mã giỏ hàng',required=True)
    name  = fields.Char(string = 'Name', help = 'Tên giỏ hàng',required=True)
    start_date = fields.Datetime(string = 'Start Date', help = 'Thời gian bắt đầu đợt mở bán của 1 đại lý, thời gian này TG (= [start_date_dotmoban,end_date_dotmoban]')
    end_date = fields.Datetime(string = 'End Date', help = 'Thời gian kết thúc đầu đợt mở bán của 1 đại lý, thời gian này TG (= [start_date_dotmoban,end_date_dotmoban]')
    opening_saleId = fields.Many2one('customer.opening.sale', string = 'Opening Sale')
    product_id = fields.Many2many('product.product',
    "cart_product_rel", 'cart_id', 'product_id', string ='Product', help ='Danh sách của các sản phẩm trong đợt mở bán')
    agency_id = fields.Many2one('res.partner', string = 'Agency', help='Những đại lý trong đợt mở bán đó',  domain="[('agency', '=', True)]", required = True)
    status = fields.Selection([
        ('1','Chưa thanh toán'),
        ('2','Đã thanh toán')
        ], string = 'Cart Status', default = '1',help = "Diễn tả tình trạng của giỏ hàng")
    is_paid = fields.Boolean(string='Đã thanh toán'
                            , help = 'Tình trạng giỏ hàng đã thanh toán hay chưa'
                            , default = False)
    opening_sale_contract_ids = fields.One2many('opening.sale.contract', 'cart_id')
    opening_sale_contract_id = fields.Many2one('opening.sale.contract'
                                            , compute = 'contract_compute')
    is_contract_status = fields.Boolean(string = "Contract Status"
                                    , default = True
                                    , compute = 'compute_contact_status' )  
    opening_sale_contract_id = fields.Many2one('opening.sale.contract', 
                                            compute = 'compute_opening_sale_contract')
    contract_status = fields.Selection(related = 'opening_sale_contract_id.contract_status')

    _sql_constraints = [
        ('date_check', "CHECK ( (start_date <= end_date))", "Ngày bắt đầu phải nhỏ ngày kết thúc!")
    ]
    
    @api.one
    @api.depends('opening_sale_contract_ids')
    def contract_compute(self):
        if len(self.opening_sale_contract_ids) > 0:
            self.opening_sale_contract_id = self.opening_sale_contract_ids[0]

    @api.constrains('cart_code')
    def _check_cart_code_constraint(self):
        """ mã giỏ hàng phải là duy nhất """
        for x in self.filtered(lambda p: p.cart_code):
            domain = [('id', '!=', x.id), ('cart_code', '=', x.cart_code)]
            if self.search(domain):
                raise ValidationError('mã giỏ hàng phải là duy nhất!')

    @api.one
    @api.depends('opening_sale_contract_ids')
    def compute_opening_sale_contract(self):
        if len(self.opening_sale_contract_ids) > 0:
            self.opening_sale_contract_id = self.opening_sale_contract_ids[0]

    @api.onchange('opening_saleId')
    def onchange_load_products(self):
        self.opening_saleId
        self.start_date
        self.end_date       
        product_object = self.env['product.product']
        result = product_object.search([('id', 'in', self.opening_saleId.product_id.ids)])
        agency_object = self.env['res.partner']
        agency_result = agency_object.search([('id', 'in', self.opening_saleId.agency_id.ids)])
        i = 1
        for item in self.opening_saleId.cart_ids:
            if i != len(self.opening_saleId.cart_ids):
                result = result - item.product_id
                agency_result = agency_result - item.agency_id
                print("Danh sach dai ly la", agency_result)
            i+=1
        self.product_id = result

        return {'domain':{'agency_id':[('id','in',agency_result.ids)]}}

    # @api.onchange('start_date','end_date')
    # def check_cart_date(self):
    #     print("@@======>>>>>Đã vào kiểm tra ngày của giỏ hàng")
    #     if self.start_date > self.end_date:
    #             raise exceptions.ValidationError('Ngày bắt đầu > ngày kêt thúc')
    #             # print("Ngày bắt đầu > ngày kêt")
        

    def order_button(self):
        "Your Code"
        context = {
            'default_cart_id': self.id,         
            'default_is_agency': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',    # name of respective model,
            'target': 'new',
            'context': context,
        } 

    def opening_sale_contract_button(self):
        "Opeing sale contract"
        print("Đã vào hợp đồng...!!")
        context = {
            'default_cart_id': self.id,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'opening.sale.contract',    # name of respective model,
            'target': 'new',
            'context': context,
        } 


class SaleOrder(models.Model):
    _inherit = "sale.order"
    _description = "Tạo hóa đơn bán hàng cho đại lý"

    cart_id = fields.Many2one("customer.cart", string = "Cart")
    
    product_number = fields.Integer(string = "Sold Products"
                                    , default = 0
                                    , help = "Số căn mà đại lý đã bán được"
                                    , compute = 'onchange_item_sale_order_cart') 
                                    
    commission_id = fields.Many2one('commission'
                                    , string = 'Commission'
                                    , help = "Loại hoa hồng") 
    commission_rate = fields.Float(string="commission rate(%)"
                                    , help = "Tỉ lệ hoa hồng nhóm người bán sẽ nhận được"
                                    , compute = 'onchange_item_commission')                                 
    total_commission_money = fields.Monetary(string = "Total Commission"
                                    , help = "Số tiền hoa hồng mà nhóm người bán sẽ nhận được"
                                    , compute = 'onchange_item_commission')  
    is_agency = fields.Boolean('Is Agency', default=False)

    transferor_id = fields.Many2one('res.partner'
                                    , string = 'Transferor'
                                    , help = 'Người chuyển nhượng hợp đồng')
    code_promo_program_id = fields.Many2one('sale.coupon.program', string="Applied Promo Program",
        domain="[('promo_code_usage', '=', 'code_needed'), '|', ('company_id', '=', False), ('company_id', '=', company_id)]", copy=False)                                
                                                                               
    # xuất report
    @api.multi
    def print_quotation(self):
        print("====>>>>  Da vao In")
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})

        return self.env.ref('customer.action_report_saleorder')\
            .with_context(discard_logo_check=True).report_action(self)

    def action_liquidation(self):
        print("đã vào phiếu thu....",self.id)
        "Phiếu thu"
        context = {
            'default_sale_order_id': self.id,  
            'default_payment_type' : 'inbound', 
            'default_partner_type': 'customer',
            'default_is_transfer': False,                 
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.payment',    # name of respective model,
            'target': 'new',
            'context': context,
        }

    def action_transfer(self):
        print("Đã vào chuyển nhượng....")
        "Chuyển nhượng"
        context = {
            'default_sale_order_id': self.id,
            'default_payment_type' : 'inbound', 
            'default_partner_type': 'customer',  
            'default_is_transfer': True,                           
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.payment',    # name of respective model,
            'target': 'new',
            'context': context,
        }
    def action_confirm_order(self):
        print("@@=====>>>>>>>Đã vào xác thực")
        for rec in self:
            print("@@=========================>Giá trị của giỏ hàng là:", rec.cart_id)
            rec.cart_id.write({'is_paid': True, 'status': '2'})
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                'It is not allowed to confirm an order in the following states: %s'
            ) % (', '.join(self._get_forbidden_state_confirm())))

        for order in self.filtered(lambda order: order.partner_id not in order.message_partner_ids):
            order.message_subscribe([order.partner_id.id])
        self.write({
            'state': 'sale',
            'confirmation_date': fields.Datetime.now()
        })
        self._action_confirm()
        if self.env['ir.config_parameter'].sudo().get_param('sale.auto_done_setting'):
            self.action_done()
        return True    

    @api.onchange('cart_id')
    def onchange_item_sale_order_cart(self):
        
        self.cart_id
        # self.product_ids = [(6, 0, self.cart_id.product_id.ids)]
        product_object = self.env['product.product']
        product = product_object.search(['&',('id', 'in', self.cart_id.product_id.ids),('is_check', '=', True)])
        print("Danh sach san pham la", product)
        self.product_number = len(product)

        order_lines = []
        for line in product:
            order_lines.append((0,0,{
                'name': line.name,
                'product_id': line.id,
                'product_uom_qty': 1,
                'tax_id': line.taxes_id,
                'price_unit': line.lst_price,

            }))
        print("order_lines:=======>",order_lines)    
        self.order_line = order_lines
        return {'domain':{'partner_id':[('id','=',self.cart_id.agency_id.ids)]
                            }}
    def _get_applicable_programs(self):
        """
        This method is used to return the valid applicable programs on given order.
        param: order - The sale order for which method will get applicable programs.
        """
        print("COUPON=====Đã vào _get_applicable_programs")
        self.ensure_one()
        programs = self.env['sale.coupon.program'].search([
        ])._filter_programs_from_common_rules(self)
        print("COUPON=====Đã vào _get_applicable_programs:::::1")
        if self.promo_code:
            programs._filter_promo_programs_with_code(self)
            print("COUPON=====Đã vào _get_applicable_programs:::::2")
        print("COUPON=====Đã vào _get_applicable_programs:::::3", programs)    
        return programs

    def _get_no_effect_on_threshold_lines(self):
        print("6::::COUPON----SALE_ORDER====>>> Đã vào _get_no_effect_on_threshold_lines")
        self.ensure_one()
        lines = self.env['sale.order.line']
        # Do not count already applied promo_code discount; Do not substract itself
        if self.code_promo_program_id and self.code_promo_program_id.reward_type == 'discount':
            lines = self.order_line.filtered(lambda l: l.product_id == self.code_promo_program_id.discount_line_product_id)
        return lines    

    # def _get_no_effect_on_threshold_lines(self):
    #     print("6::::COUPON----SALE_ORDER====>>> Đã vào _filter_on_mimimum_amount")
    #     self.ensure_one()
    #     # Do not count shipping and free shipping
    #     free_delivery_product = self.env['sale.coupon.program'].search([('reward_type', '=', 'free_shipping')]).mapped('discount_line_product_id')
    #     print("6::::free_delivery_product: ", free_delivery_product)
    #     lines = self.order_line.filtered(lambda line: line.is_delivery or line.product_id in free_delivery_product)
    #     return lines + super(SaleOrder, self)._get_no_effect_on_threshold_lines()    

    @api.onchange('commission_id') 
    def onchange_item_commission(self):
        sum_money = 0
        for record in self:          
            print("============>>>>commission:::::::",record.commission_id.commission_calculator_ids)
            # record.commission_rate = record.total_commission_money = 0.0        
            for x in record.commission_id.commission_calculator_ids:
                print("Bán được số căn từ:", x.from_number, "Đến căn:",x.to_number, "Số căn bán được:",record.product_number)
                if record.product_number >= x.from_number and record.product_number <= x.to_number:
                    print("tỉ lệ là:",x.commission)
                    record.commission_rate = x.commission
                    sum_money = record.commission_rate*record.amount_total/100
                    record.update({
                        'total_commission_money': sum_money,
                    })
                    print("Tổng tiền hoa hồng là:", sum_money)
            print("Tổng tiền hoa hồng 2 là:", sum_money)        

class Opening_Sale_Contract(models.Model):
    _name = 'opening.sale.contract'

    name = fields.Char(string='Contract Name'
                    , help='Tên hợp đồng'
                    , required = True)
    cart_id = fields.Many2one('customer.cart'
                            , string='Cart'
                            , help='hợp đồng của giỏ hàng trong đợt mở bán')
    product_ids = fields.Many2many('product.product' 
                            , 'opening_sale_contract_product_rel'
                            , 'opening_sale_contract_id'
                            , 'product_id'
                            , string = 'Products'
                            , help = 'Danh sách sản phẩm mà đại lý đó nhận để bán') 
    Date_signed = fields.Datetime(string = 'Date Signed'
                            , help = "Ngày kí kết nhận sản phẩm giữa đại lý và nhà cung cấp")

    total_deposit = fields.Float(string = "Total Deposit"
                                    , help = "Tổng số tiền mà đại lý đặt cọc cho chủ đầu tư"                                    
                                    )       
    contract_status = fields.Selection([("1","Chưa kí"),("2", "Đã kí")]
                                    ,string = "Contract Status"
                                    , help = "Tình trạng của hợp đồng"
                                    , default = "1")  

    color = fields.Integer(string = "Color"
                            , help="Màu sắc"
                            , compute='compute_color')
    def compute_color(self):
        for record in self:
            color = 0
            if record.contract_status == '1':
                color = 1
            elif record.contract_status == '2':
                color = 2         
            record.color = color                                                                          
    # Đại lý
    agency_id = fields.Many2one('res.partner'
                                , string = 'Agency'
                                , help = 'Thông tin về nhà đại lý đó')
    agency_street = fields.Char(related = 'agency_id.street')   
    agency_ward = fields.Char(related = 'agency_id.ward') 
    agency_district = fields.Char(related = 'agency_id.district')   
    agency_city = fields.Char(related = 'agency_id.city') 
    agency_state_id = fields.Many2one('res.country.state',related = 'agency_id.state_id')  
    agency_country_id = fields.Many2one('res.country', related = 'agency_id.country_id')
    agency_phone = fields.Char(related = 'agency_id.phone')
    agency_vat = fields.Char(related = 'agency_id.vat')
    representative_A = fields.Many2one('res.partner',string='Agency Representative',domain="[('is_company', '=', False)]")
    representative_posA = fields.Char(related = 'representative_A.function')
    # nhà cung cấp                      
    vendor_id = fields.Many2one('res.partner'
                                , string = 'Vendor'
                                , help = 'Thông tin về nhà cung cấp'
                                , domain = [('supplier','=', True)]) 
    vendor_street = fields.Char(related = 'vendor_id.street')   
    vendor_ward = fields.Char(related = 'vendor_id.ward')
    vendor_district = fields.Char(related = 'vendor_id.district')
    vendor_city = fields.Char(related = 'vendor_id.city') 
    vendor_state_id = fields.Many2one('res.country.state',related = 'vendor_id.state_id')  
    vendor_country_id = fields.Many2one('res.country', related = 'vendor_id.country_id')
    vendor_phone = fields.Char(related = 'vendor_id.phone')
    vendor_vat = fields.Char(related = 'vendor_id.vat')
    representative_B= fields.Many2one('res.partner',string='Vendor Representative',domain="[('is_company', '=', False)]")
    representative_posB = fields.Char(related = 'representative_B.function')

    product_agent_received = fields.Integer(string = 'Product Received'
                                            , help = 'Số căn nhà mà đại lý đó nhận để bán'
                                            , default = 0)  
    # total_amount_product = fields.Monetary(string )
    #Phụ lục hợp đồng
    op_annex_id = fields.Many2many('opening_sale_contract_annex',string = 'Contract Annex')  

    @api.onchange('cart_id')
    def onchange_item_cart(self):
        tong = 0
        print("---------------->>>>>Đang vào hợp đồng đợt mở bán")
        for record in self:
            print ("cart id là:",record['cart_id'])
            record["product_ids"] = [(6, 0, record.cart_id.product_id.ids)]  
            tong = len(record["product_ids"])
            print("số sản phẩm trong hóa đơn đó là:", tong)
            record.product_agent_received = tong
            # for x in record.cart_id.product_id.ids:
            #     sum += 1
        return {'domain':{'agency_id':[('id','=',self.cart_id.agency_id.ids)]}}
    
    
class OpeningSale_ContractAnnex(models.Model):
    _name = 'opening_sale_contract_annex'
    
    op_annex_id = fields.Char(string = 'Annex Contract ID',help = 'Mã phụ lục của hợp đồng')
    op_name_annex = fields.Char(string = 'Annex Contract ID Name'
                                ,help = 'Tên điều khoản'
                                , required = True)
    op_description_annex = fields.Text(string = 'Content',help = 'Nội dung điều khoản') 


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_type = fields.Selection(related = "product_id.product_type")
    is_check = fields.Boolean(related = "product_id.is_check")
    project_id = fields.Many2one(related='product_id.project_id')
    is_delivery = fields.Boolean(string="Is a Delivery", default=False)

    _sql_constraints = [
        ('accountable_required_fields', 'CHECK(1=1)', "Another asset already exists with this serial number!"),
    ]

class account_payment(models.Model):
    _inherit = "account.payment"

    sale_order_id = fields.Many2one('sale.order', string = 'Sale Order')
    is_transfer = fields.Boolean("Is Transfer", default = False)

    @api.onchange('sale_order_id')
    def onchange_sale_order(self):
        print("khách hàng chuyển nhượng ...")
        self.sale_order_id   
        for rec in self:
            print('Đúng là chuyển nhượng.....',rec.is_transfer)
        if self.is_transfer == False:        
            return {'domain':{'partner_id':[('id','=',self.sale_order_id.partner_id.ids)]}}

    @api.multi    
    def action_post(self):
        print("Đã vào....")      
        for rec in self:
            print("Giá trị chuyển nhượng là:", rec.is_transfer)
            print("Giá trị của sale order::", rec.sale_order_id)
            if rec.is_transfer == False:
                rec.sale_order_id.write({'state': 'cancel'})
            elif rec.is_transfer == True:
                print("Tên người chuyển nhượng là:", rec.partner_id)
                print("Giá trị của order_line là:", rec.sale_order_id.order_line)
                print("Giá trị của người người chuyển nhượng là:", rec.sale_order_id.partner_id.id)
                order_lines = []
                for line in rec.sale_order_id.order_line:
                    order_lines.append((0,0,{
                        'name': line.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'tax_id': line.tax_id,
                        'price_unit': line.price_unit,
                        
                    }))
                print("Giá trị của order lines là:", order_lines)    
                self.env['sale.order'].create({
                    'partner_id': rec.partner_id.id, 
                    'partner_invoice_id': rec.partner_id.id, 
                    'partner_shipping_id': rec.partner_id.id,                   
                    'order_line': order_lines,
                    'transferor_id': rec.sale_order_id.partner_id.id,
                    })
                rec.sale_order_id.write({'state': 'cancel'})    
                # rec.sale_order_id.write)

            if rec.state != 'draft':
                raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
        return True

   



   
