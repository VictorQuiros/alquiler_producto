# alquiler_producto/__manifest__.py
{
    'name': 'Alquiler de Productos',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Gestión de alquiuler de productos.',
    'description': """
    Módulo para gestionar los alquileres de productos de los clientes.
    """,
    'author': 'Victor Quiros',
    'depends': ['base', 'sale', 'stock'], # Requiere módulos base, ventas e inventario
    'data': [
    'views/alquiler_producto_views.xml',
    'security/ir.model.access.csv',
    ],
    'icon': '/alquiler_producto/static/description/icon55.png',
    'installable': True,
    'application': True,
}