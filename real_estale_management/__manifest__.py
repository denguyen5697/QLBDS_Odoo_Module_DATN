# -*- coding: utf-8 -*-
{
    'name': "Bat Dong San",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Catagory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'contacts', 'product', 'project', 'sale_management', 'sale', 'crm', 'website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'demo/demo.xml',
        #****************************               MASTER DATA                    **************************************
        #================================================================================================================
        #================================================================================================================
        # customer
        'views/master_data/customers/customer_view.xml',
        'views/master_data/customers/customer_group_view.xml',
        'views/master_data/partner.xml',

        # product
        # 'views/master_data/products/product_template_view.xml',
        'views/master_data/products/product_product_view.xml',
        'views/master_data/products/product_category_view.xml',
        

        # saleteam
        'views/master_data/saleteams/saleteam_view.xml',

        #uom
        'views/master_data/uom/uom_view.xml',
        'views/master_data/uom/uom_category_view.xml',

        # #vendor
        # 'views/master_data/vendors/vendor_view.xml',
        # 'views/master_data/vendors/agency_view.xml',

        # project
        'views/master_data/projects/project_view.xml',
        'views/master_data/projects/project_type_view.xml',
        'views/master_data/projects/project_legal_view.xml',

        #*************************            TRANSACTION MANAGERMENT        **********************************************
        #==================================================================================================================
        #=================================================================================================================
        
        #cart
        'views/transaction_management/carts/cart_view.xml',
        'views/transaction_management/carts/pricelists_view.xml',

        # contract
        'views/contracts/contract_view.xml',
        'views/contracts/contract_annex_view.xml',
        'views/contracts/status_transaction_view.xml',
        'views/contracts/contract_report.xml',
        'views/contracts/contract_report_template.xml',

        # commission
        'views/transaction_management/commissions/commission_view.xml',

        # opening_sale
        'views/transaction_management/opening_sale/opening_sale_view.xml',
        'views/transaction_management/opening_sale/opening_sale.xml',
        'views/transaction_management/opening_sale/opening_sale_contract_view.xml',
        'views/transaction_management/opening_sale/opening_sale_contract_annex.xml',
        

        # promotion_programs
        # 'views/transaction_management/sale_order/sale_order_inherit.xml',
        'views/transaction_management/promotion_programs/promotions_program_views.xml',
        # 'views/transaction_management/promotion_programs/sale_coupon_program_views.xml',
        
        # sale order
        'views/orders/order_view.xml',
        'views/orders/sale_report_templates.xml',
        'views/orders/sale_report.xml',

        # setting
        'views/configurations/settings_view.xml',

        #payments
        'views/payments/account_payment_view.xml',

        # wizard
        'wizard/sale_coupon_apply_code_views.xml',
        'wizard/sale_coupon_generate_views.xml',

        # sale_management
        'views/transaction_management/sale_management/cron.xml',
        # 'views/transaction_management/sale_management/payment_info_view.xml',
        'views/transaction_management/sale_management/transaction_manager_view.xml',

        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
