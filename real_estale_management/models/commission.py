from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo import exceptions

class Commission(models.Model):
    # Ingerit from Res Partner
    _name = "commission"

    name = fields.Char(string = 'Commission'
                        , help = 'Tên hoa hồng', required = True)
    commission_calculator_ids = fields.One2many('commission.calculator'
                                            , 'commission_id'
                                            )                    
    # commission_calculator_ids = fields.Many2many('commission.calculator'
    #                                             ,'commission_calculator_rel'
    #                                             , 'commission_id'
    #                                             , 'commission_calculator_id'
    #                                             , string = 'Commission')

class CommissionCalculator(models.Model):  
    _name = "commission.calculator"                                                                 
    
    from_number = fields.Integer(string = 'From Number'
                        , help = 'Hoa hồng bán được số căn từ' 
                        , default = 0)
    to_number = fields.Integer(string = 'To Number'
                        , help = 'Hoa hồng bán được số căn đến'
                        , default = 0) 
    commission = fields.Float(string = 'Commmission (%)'
                        , help = 'Tỉ lệ hoa hồng'
                        , default = 0.0)
    commission_id = fields.Many2one('commission')  


  
    @api.multi
    @api.constrains('from_number', 'to_number', 'commission')
    def to_number_constrains(self):
        last_id = self.env['commission.calculator'].search([])[-1]
        print('Số căn cuối cùng là:',last_id)
        for rec in self:
            if rec.from_number > rec.to_number:
                raise exceptions.ValidationError('To Number phải lớn hơn From Number!')
            elif rec.commission < 0 or rec.commission > 100:
                raise exceptions.ValidationError('Hoa hồng phải thuộc (0,100)')
            # else:
            #     for item in last_id:
            #        if rec.from_number < item.to_number:
            #             raise exceptions.ValidationError('Giá trị nhập không hợp lệ vui lòng kiểm tra lại!, Tại Number to:')


    # @api.onchange('from_number')
    # def onchange_from_number(self):   
    #     last_id = self.env['commission.calculator'].search([])[-1]
    #     # obj = env[MODEL]
    #     for rec in self:                
    #         for item in last_id:
    #            if rec.from_number < item.to_number:
    #                 raise exceptions.ValidationError('Giá trị nhập không hợp lệ vui lòng kiểm tra lại!!!')
                        
   
    

    
    
      
        


    

