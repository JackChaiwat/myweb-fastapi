from sqladmin import ModelView, BaseView
from sqladmin import expose
from models import Product, Order, OrderDetail


class ProductAdmin(ModelView, model=Product):
    name = "Product"
    name_plural = "Products"
    category = "Inventory"
    list_template = "list.html" 

    column_list = [
        Product.id,
        Product.name,
        Product.category,
        Product.price
    ]
    column_labels = {
        Product.id: "รหัสสินค้า",
        Product.name: "ชื่อสินค้า",
        Product.category: "ประเภทสินค้า",
        Product.price: "ราคา"
    }
    column_searchable_list = [
        Product.name
    ]
    column_sortable_list = [
        Product.id,
        Product.name,
        Product.price
    ]
    form_columns = [
        Product.name,
        Product.price,
        Product.category,
    ]
    
    async def after_model_change(self, data, model, is_created, request):
        request.session["flash"] = "Product saved successfully"


class UploadView(BaseView):
    name = "Upload Images"
    icon = "fa-solid fa-upload"
    @expose("/upload", methods=["GET"])
    async def upload(self, request):
        return await self.templates.TemplateResponse(
            request,
            "upload.html",
            {"request": request}
        )
